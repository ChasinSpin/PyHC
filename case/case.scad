// Print with support (needed for the switch and battery door)
// Need 6 x Hanglife M3 inserts and 6 Counter sunk M3 x 20

partNum                     = 1;        // 0 = All assembled, 1 = All ready for printing, 2 = bottom, 3 = top, 4 = Battery base, 5 = batteryDoor

border                      = 3.0;
caseCornerRadius            = 4.0;
caseInsideDimensions        = [65, 120, 31];
caseOutsideDimensions       = [caseInsideDimensions[0] + border * 2, caseInsideDimensions[1] + border * 2, caseInsideDimensions[2] + border * 2];
switchOutsideDiameter       = 18.0;
switchHoleDiameter          = 13.5;
switchLocatorInset          = 0.5;

switchLocationsOffsetY      = 0;
switchLocations             = [ [0, -45], [-20, 0], [20, 0], [0, -20], [0, 20], [-20, -45], [20, -45] ];
biColorButtonsLocations     = [ [-20, 0], [20, 0], [0, -20], [0, 20] ];

caseJoiningPostLocations    = [ [-31, -57], [-31, -12], [-31, 57], [31, -57], [31, -12], [31, 57] ];
caseJoiningPostDiameter     = 8.0;

m3InsertDiameter            = 4.35 + 0.3;
m3InsertDepth               = 5.0;
m3BoltHoleDiameter          = 3.2;
m3BoltHoleDepth             = caseOutsideDimensions[2] / 2 - border;
m3HeadDiameter              = 7.0;
m3HeadHeight                = 2.0;

featherOffset               = [1, 45];
featherDimensions           = [51, 23, 10];
featherDisplayDimensions    = [27, 17, 2];

featherPostHeight           = 2.6 ;
featherBoltPostDiameter     = 6.0;
featherBoltPostHoleDiameter = 2.1;
featherBoltPostHoleDepth    = featherPostHeight + border - 1.0;
featherBoltPostHolePositions= [2.5, 2.5];
featherSupportPostPositions = [2.65, 2.0];
featherSupportPostDiameter  = 5.0;
featherSupportPostPostDia   = 2.2;
featherSupportPostPostHeight= 1.5;

featherSupportMatingDiameter= 2.6;
featherSupportMatingHeight  = 6.4;

mapLEDHoleDiameter          = 3.0;
mapLEDHoleOffset            = [3.55, 3.61];

resetHoleDiameter           = 2.2;
resetHoleOffset             = [19.5, 0];

lanyardInsideHoleDiameter   = 6.0;
lanyardOutsideHoleDiameter  = 12.0;
lanyardHeight               = 5.0;
lanyardLoopOffsetX          = 25;

usbPortDimensions           = [20, 13, 8.6];
usbPortOffsetZ              = 3.36 + 0.3;

caseSplitHeight             = 21.5;
caseTopHeight               = caseSplitHeight;
caseBottomHeight            = caseOutsideDimensions[2] - caseSplitHeight;
caseTopSplitOffsetZ         = 0;
caseBottomOffsetZ           = caseSplitHeight;

boltHeadDepth               = 10.0;

batteryBaseThickness        = 2.0;
batteryBasePwrDiameter      = 5.0;
batteryBasePwrOffsetXY      = [17.0, 48];

biColorRingDiameter         = 20.25;
biColorDepth                = 0.6;
biColorOutsideWidth         = 3.0;

manifoldCorrection          = 0.01;
manifoldCorrection2         = manifoldCorrection * 2;

batterySliderFlangeWidth    = 2.0;
batterySliderDimensions     = [50, 85, border/2 + manifoldCorrection];
batterySliderInnerDimension = [batterySliderDimensions[0] - batterySliderFlangeWidth * 2, batterySliderDimensions[1] - batterySliderFlangeWidth, border/2 + manifoldCorrection2];
batterySliderCaseReinforcementDimensions    = [batterySliderDimensions[0] + batterySliderFlangeWidth * 2, batterySliderDimensions[1] + batterySliderFlangeWidth, batterySliderFlangeWidth];
batteryDoorScaling          = [0.99, 0.99, 0.5];
batteryDoorLocatorDiameter  = batterySliderFlangeWidth;
batteryDoorLocatorWidth     = 20;
batteryDoorLocatorOffsetY   = border + batteryDoorLocatorDiameter/2 - 0.4 + 2.0;
batteryDoorLocatorOffsetZ   = 2.3 - 1.0;
batteryDoorNotchDimensions  = [30, 4, 1];
batteryDoorNotchSpacing     = 7;

powerSwitchDimensions       = [13.25 + 0.3, border + manifoldCorrection2, 8.85 + 0.3];
powerSwitchOffsetZ          = border + 4;



if ( partNum == 0 )
{
    caseBottom();
    caseTop();
}

if ( partNum == 1 )
{
    caseBottom();
    translate( [-caseOutsideDimensions[0] - 10, 0, caseOutsideDimensions[2]] )
        rotate( [0, 180, 0] )
            caseTop();
    translate( [caseOutsideDimensions[0] + 10, 0, 0] )
        batteryBase();
        
    translate( [-15, caseOutsideDimensions[1]/2 + batterySliderDimensions[1]/2 - 5, 0] )
        rotate( [0, 0, 90] )
            batteryDoor();
}

if ( partNum == 2)
    caseBottom();

if ( partNum == 3)
    translate( [-caseOutsideDimensions[0] - 10, 0, caseOutsideDimensions[2]] )
        rotate( [0, 180, 0] )
            caseTop();

if ( partNum == 4)
    batteryBase();

if ( partNum == 5)
    batteryDoor();

            
module caseBottom()
{
    difference()
    {
        case();
        translate( [0, 0, caseBottomHeight / 2 + caseBottomOffsetZ] )
            cube( [caseOutsideDimensions[0]*2 + manifoldCorrection2, caseOutsideDimensions[1]*2 + manifoldCorrection2, caseBottomHeight + manifoldCorrection], center = true ); 
    }    
}



module caseTop()
{
    difference()
    {
        case();
        translate( [0, 0, caseTopHeight / 2 + caseTopSplitOffsetZ - manifoldCorrection] )
            cube( [caseOutsideDimensions[0]*2 + manifoldCorrection2, caseOutsideDimensions[1]*2 + manifoldCorrection2, caseTopHeight + manifoldCorrection], center = true ); 
    }
}



module batteryBase()
{
    difference()
    {
        roundedCube( [caseOutsideDimensions[0], caseOutsideDimensions[1], batteryBaseThickness], radius = caseCornerRadius );
    
        // Bolt holes
        for ( posXY = caseJoiningPostLocations )
            translate( [posXY[0], posXY[1], 0] )
                translate( [0, 0, -manifoldCorrection] )
                    cylinder(d = m3BoltHoleDiameter, h = batteryBaseThickness + manifoldCorrection2, $fn = 40);
                    
        // Map LED Hole
        translate( [featherOffset[0], featherOffset[1], 0] )
            translate( [mapLEDHoleOffset[0], mapLEDHoleOffset[1], -manifoldCorrection] )
                cylinder(d = mapLEDHoleDiameter * 5, h = batteryBaseThickness + manifoldCorrection2, $fn = 40);     
         
        // Power hole
        translate( [batteryBasePwrOffsetXY[0], batteryBasePwrOffsetXY[1], -manifoldCorrection] )
            cylinder(d = batteryBasePwrDiameter, h = batteryBaseThickness + manifoldCorrection2, $fn = 40);
    }
    
        // Posts to push against the back of the board on the non-screwed positions
    featherPostOffset = featherDimensions[1]/2 - featherSupportPostPositions[1];
    translate( [featherOffset[0] + featherDimensions[0]/2 - featherSupportPostPositions[0], featherOffset[1], 0] )
            {
                for ( posY = [featherPostOffset, -featherPostOffset] )
                    translate( [0, posY, 0] )
                    {
                        cylinder(d = featherSupportPostDiameter, h = batteryBaseThickness + 8.25 - 1.5, $fn = 40);
                        cylinder(d = featherSupportMatingDiameter, h = batteryBaseThickness + 8.25, $fn = 40);
                    }
            }

}



module surroundHighlight()
{
    difference()
    {
        roundedCube( [caseOutsideDimensions[0] + manifoldCorrection2, caseOutsideDimensions[1] + manifoldCorrection2, biColorDepth], radius = caseCornerRadius );
        translate( [0, 0, -manifoldCorrection] )
            roundedCube( [caseOutsideDimensions[0] - biColorOutsideWidth*2, caseOutsideDimensions[1] - biColorOutsideWidth*2, biColorDepth + manifoldCorrection2], radius = caseCornerRadius );
    }
}


module biColorButtonRing()
{
    cylinder(d = biColorRingDiameter, h = biColorDepth);
}



module batterySlider()
{
    translate( [-batterySliderDimensions[0] / 2, -caseOutsideDimensions[1]/2, 0] )
    {
        translate( [batterySliderFlangeWidth, 0, -manifoldCorrection] )
            cube( batterySliderInnerDimension );
        translate( [0, 0, border/2] )
            cube( batterySliderDimensions );
    }
}


module batterySliderCaseReinforcement()
{
    translate( [-batterySliderCaseReinforcementDimensions[0] / 2, -caseOutsideDimensions[1]/2, border] )
        difference()
        {
            cube(batterySliderCaseReinforcementDimensions);
            
            translate( [batterySliderFlangeWidth * 2, 0, -manifoldCorrection] )
                cube( [batterySliderInnerDimension[0], batterySliderInnerDimension[1], border + manifoldCorrection2] );
        }
}



module batteryDoor()
{
    difference()
    {
        union()
        {
            scale( batteryDoorScaling )
                batterySlider();
        
            translate( [0, -caseOutsideDimensions[1]/2 + batteryDoorLocatorOffsetY, batteryDoorLocatorOffsetZ] )
                rotate( [0, 90, 0] )
                    cylinder( d = batteryDoorLocatorDiameter, h = batteryDoorLocatorWidth, center = true, $fn = 40);
        }
        
        for ( posY = [0, batteryDoorNotchSpacing, batteryDoorNotchSpacing*2, batteryDoorNotchSpacing*3] )
            translate( [0, -caseOutsideDimensions[1]/2 + batteryDoorNotchSpacing + posY, -0.1] )
                translate( [-batteryDoorNotchDimensions[0]/2, -batteryDoorNotchDimensions[1]/2, 0] )
                    cube( batteryDoorNotchDimensions );
    }
}



module case()
{
    featherBoltPostOffset = featherDimensions[1]/2 - featherBoltPostHolePositions[1];
    featherPostOffset = featherDimensions[1]/2 - featherSupportPostPositions[1];

    difference()
    {
        union()
        {
            difference()
            {
                union()
                {
                    difference()
                    {
                        roundedCube( caseOutsideDimensions, radius = caseCornerRadius );
                
                                
                        // Bi color rings
                        translate( [0, 0, caseOutsideDimensions[2] - biColorDepth] )
                            for ( posXY = biColorButtonsLocations )
                                translate( [posXY[0], posXY[1] + switchLocationsOffsetY, 0] )
                                    biColorButtonRing();
                    }
                
                    // Bi color rings
                    color( [1.0, 0.0, 0.0] )
                        translate( [0, 0, caseOutsideDimensions[2] - biColorDepth + 0.001] )
                            for ( posXY = biColorButtonsLocations )
                                translate( [posXY[0], posXY[1] + switchLocationsOffsetY, 0] )
                                    biColorButtonRing();
                }
        
                translate( [0, 0, caseInsideDimensions[2]/2 + (caseOutsideDimensions[2] - caseInsideDimensions[2]) / 2] )
                    cube( caseInsideDimensions, center = true );

                translate( [0, 0, caseOutsideDimensions[2] - border - manifoldCorrection] )
                {
                    // Switches
                    for ( posXY = switchLocations )
                        translate( [posXY[0], posXY[1] + switchLocationsOffsetY, 0] )
                            cylinder(d = switchHoleDiameter, h = border + manifoldCorrection2, $fn = 40);

                    // Feather Display      
                    translate( featherOffset )
                        translate( [0, 0, border/2 + manifoldCorrection] )
                            cube( [featherDisplayDimensions[0], featherDisplayDimensions[1], border + manifoldCorrection2] , center = true ); 
                }
                

                // Bi color surround
                translate( [0, 0, caseOutsideDimensions[2] - biColorDepth] )
                    surroundHighlight();
                
                translate( [0, -manifoldCorrection, 0] )
                    batterySlider();
            }
            
            // Bi color surround
            translate( [0, 0, caseOutsideDimensions[2] - biColorDepth + 0.001] )
                color( [1.0, 0.0, 0.0] )
                    surroundHighlight();

            // The square part of the switch hole
            translate( [-switchHoleDiameter/2, 0, caseOutsideDimensions[2] - border] )
            {
                // Switches
                for ( posXY = switchLocations )
                    translate( [posXY[0], posXY[1] + switchLocationsOffsetY - switchHoleDiameter/2, 0] )
                        cube( [switchLocatorInset, switchHoleDiameter, border] );
            }
                        
            for ( posXY = caseJoiningPostLocations )
                translate( [posXY[0], posXY[1], 0] )
                    cylinder(d = caseJoiningPostDiameter, h = caseOutsideDimensions[2], $fn = 40 );

            // Feather mounting posts
            translate( [featherOffset[0] - featherDimensions[0]/2 + featherBoltPostHolePositions[0], featherOffset[1], caseOutsideDimensions[2] - featherPostHeight - border] )
            {
                for ( posY = [featherBoltPostOffset, -featherBoltPostOffset] )
                    translate( [0, posY, 0] )
                        cylinder(d = featherBoltPostDiameter, h = featherPostHeight, $fn = 40);
            }

            translate( [featherOffset[0] + featherDimensions[0]/2 - featherSupportPostPositions[0], featherOffset[1], caseOutsideDimensions[2] - featherPostHeight - border] )
            {
                for ( posY = [featherPostOffset, -featherPostOffset] )
                    translate( [0, posY, 0] )
                    {
                        cylinder(d = featherSupportPostDiameter, h = featherPostHeight, $fn = 40);
                        translate( [0, 0, -featherSupportPostPostHeight] )
                           cylinder(d = featherSupportPostPostDia, h = featherSupportPostPostHeight, $fn = 40);
                    }
            }
        }
        
        // m3 insert holes and bolt holes
        for ( posXY = caseJoiningPostLocations )
            translate( [posXY[0], posXY[1], 0] )
            {
                // Insert holes
                translate( [0, 0, caseTopHeight - manifoldCorrection] )
                    cylinder(d = m3InsertDiameter, h = m3InsertDepth, $fn = 40);

                // Bolt holes
                translate( [0, 0, -manifoldCorrection] )
                {
                    cylinder(d = m3BoltHoleDiameter, h = caseOutsideDimensions[2] - border * 2 + manifoldCorrection, $fn = 40);
                    cylinder(d = m3HeadDiameter, h = boltHeadDepth + manifoldCorrection, $fn = 40);
                    translate( [0, 0, boltHeadDepth] )
                        cylinder(d1 = m3HeadDiameter, d2 = m3BoltHoleDiameter, h = m3HeadHeight + manifoldCorrection, $fn = 40);
                }
            }
            
            
        // Feather mounting post holes
        translate( [featherOffset[0] - featherDimensions[0]/2 + featherBoltPostHolePositions[0], featherOffset[1], caseOutsideDimensions[2] - featherPostHeight - border] )
        {
            for ( posY = [featherBoltPostOffset, -featherBoltPostOffset] )
                translate( [0, posY, -manifoldCorrection] )
                    cylinder(d = featherBoltPostHoleDiameter, h = featherBoltPostHoleDepth, $fn = 40);
        }
        
        // Map LED Hole
        translate( [featherOffset[0], featherOffset[1], 0] )
            translate( [mapLEDHoleOffset[0], mapLEDHoleOffset[1], -manifoldCorrection] )
                cylinder(d = mapLEDHoleDiameter, h = border + manifoldCorrection2, $fn = 40);
                
        // Reset Hole
        translate( [featherOffset[0], featherOffset[1], caseOutsideDimensions[2]] )
            translate( [resetHoleOffset[0], resetHoleOffset[1], -border - manifoldCorrection] )
                cylinder(d = resetHoleDiameter, h = border + manifoldCorrection2, $fn = 40);
                
        // USB Hole
        translate( [-caseOutsideDimensions[0]/2 + border/2, featherOffset[1], caseOutsideDimensions[2] - featherPostHeight - border -usbPortOffsetZ] )
            cube( [usbPortDimensions[0] + manifoldCorrection2, usbPortDimensions[1], usbPortDimensions[2]], center = true );

        // Power switch
        translate( [0, -caseOutsideDimensions[1]/2 + border/2, powerSwitchDimensions[2]/2 + powerSwitchOffsetZ] )
            cube( powerSwitchDimensions, center = true);
    }
    
    for ( posX = [-lanyardLoopOffsetX, lanyardLoopOffsetX] )
        translate( [posX, -caseOutsideDimensions[1] / 2 - lanyardInsideHoleDiameter/2, caseOutsideDimensions[2] - lanyardHeight] )
            lanyardLoop();
            
     // Battery slider case reinforcement
     batterySliderCaseReinforcement();
     
    //%feather();
}



module lanyardLoop()
{
    difference()
    {
        union()
        {
            cylinder(d = lanyardOutsideHoleDiameter, h = lanyardHeight, $fn = 40);
            translate( [-lanyardOutsideHoleDiameter/2, 0, 0] )
                cube( [lanyardOutsideHoleDiameter, lanyardOutsideHoleDiameter/2, lanyardHeight] );
        }
        translate( [0, 0, -manifoldCorrection] )
            cylinder(d = lanyardInsideHoleDiameter, h = lanyardHeight + manifoldCorrection2, $fn = 40);
    }
}



module roundedCube(dimensions, radius)
{

    halfWidth   = dimensions[0] / 2 - radius;
    halfLength  = dimensions[1] / 2 - radius;
    
    hull()
        for ( posXY = [ [-halfWidth, -halfLength], [-halfWidth, halfLength], [halfWidth, -halfLength], [halfWidth, halfLength] ] )
            translate( [posXY[0], posXY[1], 0] )
                cylinder(r = radius, h = dimensions[2], $fn = 40);
}



module feather()
{
    translate( featherOffset )
        translate( [0, 0, featherDimensions[2]/2 + caseOutsideDimensions[2] - featherDimensions[2] - border] )
            cube( featherDimensions, center = true ); 
}