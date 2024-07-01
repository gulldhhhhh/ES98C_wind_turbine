import numpy as np
import os
import pandas as pd
from itertools import combinations

def simulate(position, sim_number):
    k=sim_number
    min_dist = 279.0
    num_turb = len(position)
    dist = np.zeros([num_turb,num_turb])
    
    # Calculate distances between all pairs of turbines
    for i, j in combinations(range(num_turb), 2):
        if (np.linalg.norm(position[i]-position[j])<min_dist):
            print("Distance between turbine ",i+1," and turbine ",j+1," is too low")
            return -1
    
    # Generate turbine and cylinder coordinates based on position
    turbine_coords = [np.array([(position[i][0]-2000),(position[i][1])]) for i in range(num_turb)]
    cylinder_coords = [np.array([(position[i][0]-2100),(position[i][1])]) for i in range(num_turb)]
    
    # Generate hexmeshdict file
    # Part 1: Preamble
    data = '''/*--------------------------------*- C++ -*----------------------------------*\ 
| =========                 |                                                 |
| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\    /   O peration     | Version:  4.x                                   |
|   \\  /    A nd           | Web:      www.OpenFOAM.org                      |
|    \\/     M anipulation  |                                                 |
\*---------------------------------------------------------------------------*/
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      snappyHexMeshDict;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
 castellatedMesh true;
 snap false;
 addLayers false;
// https://sites.google.com/site/snappywiki/snappyhexmesh/snappyhexmeshdict/user-defined-regions
geometry
{
'''
    # Part 2: Cylinders and spheres
    for i in range(num_turb):
        # 2a: Cylinder
        data = data + '''refinementCylinder{n}            
{{
 type searchableCylinder;
 point1 ({cy1_x} {tcoord_y} 63.3);
 point2 ({cy2_x} {tcoord_y} 63.3);
 radius 80.0;
}}
'''.format(n=i,cy1_x=cylinder_coords[i][0],tcoord_y=turbine_coords[i][1],cy2_x=cylinder_coords[i][1])
        # 2b: Sphere
        data = data + ''' refinementSphere{} 
{{
 type searchableSphere;
 centre ({} {} 63.3);
 radius 63.3;
}}
'''.format(i,turbine_coords[i][0],turbine_coords[i][1])
        
    # Part 3: Middle section
    data = data + '''
};
castellatedMeshControls
{
 maxLocalCells 100000;
 maxGlobalCells 10000000;
 minRefinementCells 10;
 nCellsBetweenLevels 1;
 resolveFeatureAngle 30;
 features (); 
 refinementSurfaces { };
 refinementRegions
{
'''
    # Part 4: Cylinder/sphere settings
    for i in range(num_turb):
        data = data + '''refinementCylinder{n} 
 {{
 mode inside;
 levels ((1.0 1)); // one level of general refinement
 levelIncrement (0 1 (2 2 0)); // apply two level of refinement to any level 0 cells in the x and y directions only
 }}
refinementSphere{n}
 {{
 mode inside;
 levels ((1.0 0));
 levelIncrement (0 3 (4 4 0)); // apply extra levels of directional refinement inside fine sphere.
 }}
'''.format(n=i)
        
    # Part 5: End
    data = data +'''}
 locationInMesh (0.0 0.0 63.3);
 allowFreeStandingZoneFaces true;
}
meshQualityControls
{
maxNonOrtho 65;
maxBoundarySkewness 20;
maxInternalSkewness 4;
maxConcave 80;
minFlatness 0.5;
minTetQuality 1e-30;
minVol 1e-13;
minArea -1;
minTwist 0.05;
minDeterminant 0.001;
minFaceWeight 0.05;
minVolRatio 0.01;
minTriangleTwist -1;
nSmoothScale 4;
errorReduction 0.75;
relaxed
{
 maxNonOrtho 75;
}
 nSmoothScale 4;
 errorReduction 0.75;
}
snapControls
{
 nSmoothPatch 3;
 tolerance 2.0;
 nSolveIter 30;
 nRelaxIter 5;
}
addLayersControls
{
}
mergeTolerance 1e-6;
'''
    with open(r'snappyHexMeshDict', 'w') as file:
        file.write(data)

    #Write turbine file
    data=''
    for i in range(num_turb):
        data = data + 'T{:03d} {} {}\n'.format(i,str(turbine_coords[i][0]),str(turbine_coords[i][1]))
    with open(r'xy_turbine.txt', 'w') as file:
        file.write(data)
            #execute script for creating and submitting CFD simulation
    exit_code = os.system('bash create_turbine_files_3_turbine.sh '+str(k).zfill(4)+' '+str(num_turb).zfill(2))
    print(exit_code)
        
    return 0