import arcpy, os, sys, traceback, glob
arcpy.env.overwriteOutput = True
# create a new copy and remove duplicate observations (same location)
# leaving only the first date observed
direct = 'D:\\ABoVE\\Version2.0_2016_2019_update\\'
try:
    for year in range(2019, 2020):
        print 'Processing fire progression maps for ' + str(year)

        afpath = direct + 'Output\\Round2\\' + str(year) + '\\fires_cl_split\\'
        medpath = direct + 'Output\\Round2\\' + str(year) +'\\fires_cl_split_medpath\\'
        if not os.path.exists(medpath): os.makedirs(medpath)

        #I did this 1 year at a time and changed the range max value. I can't remember why but I think it saved time in the end
        for afi in range(1, 1189): #1401 for 2012; 1529 for 2013; 1141 for 2014; 2093 for 2015; 1178 for 2016 ; 1720 for 2017; 1956 for 2018; 1189 for 2019

            origFire = afpath + str(afi)+'.shp'

            if os.path.exists(origFire):

                # Copy the original files to create the working version
                fires = medpath + str(afi) + '_fires.shp'

                arcpy.CopyFeatures_management(origFire, fires)

                # remove all unnecessary fields from fires to leave only FID, SHAPE,
                # YYYYMMDD, HHMM, LAT, LON
                fieldNames = [f.name for f in arcpy.ListFields(fires)]
                subList = fieldNames[2:]
                for s in subList:
                    if (s <> 'YYYYMMDD') and (s <> 'HHMM') and (s <> 'LAT') and (s <> 'LON') and (s <> 'TARGET_FID') and (s <> 'UID_Fire'):
                        arcpy.DeleteField_management(fires, s)
                del fieldNames, subList, s

                print 'Removed unnecessary fields from active fires\n'


                # Calulate Julian Date (JD) from YYYYMMDD (April - September)
                arcpy.AddField_management(fires, "JD_UTC", "LONG", 5)
                arcpy.AddField_management(fires, "JD", "LONG", 5)

                perpList = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
                leapList = [1, 32, 61, 92, 122, 153, 183, 214, 245, 275, 306, 336]

                if (year == 2004) or (year == 2008) or (year == 2012) or (year == 2016) or (year == 2020) or (year == 2024):
                    dList = leapList
                else:
                    dList = perpList

                for m in range(1, 13):
                    ddB = int(str(year) + (str(m)).zfill(2) + '00')
                    ddE = int(str(year) + (str(m + 1)).zfill(2) + '00')
                    expr = '"YYYYMMDD">' + str(ddB) + ' AND "YYYYMMDD" <' + str(ddE)
                    jdstart = dList[m - 1]

                    r, rows = None, None

                    rows = arcpy.UpdateCursor(fires, expr)

                    for r in rows:
                        d = r.YYYYMMDD
                        r.JD_UTC = jdstart - 1 + (d - ddB)
                        rows.updateRow(r)
                    if rows:
                        del rows
                    if r:
                        del r

                print 'Assigned Julian Date according to UTC time\n'

                # Adust JD from UTC to local time(hard -9 for Alaska)
                arcpy.AddField_management(fires, "Time_d", "FLOAT", 10, 3, 15)

                r, rows = None, None

                rows = arcpy.UpdateCursor(fires)
                for r in rows:
                    hhmmstr = r.HHMM
                    hhmm = str(hhmmstr).zfill(4)
                    # hhmm = hhmmstr.strip('')
                    # print hhmm
                    hh = float(hhmm[:2])
                    mm = float(hhmm[2:])

                    #print hh,mm

                    tdec = hh + mm / 60
                    r.JD = 0
                    r.Time_d = tdec
                    rows.updateRow(r)
                    if tdec < 9.0:
                        r.JD = r.JD_UTC - 1
                    else:
                        r.JD = r.JD_UTC
                    rows.updateRow(r)
                del rows, r

                print 'Completed adjusting the Julian date to the local time\n'

                # create a new copy and remove duplicate observations (same location)
                # leaving only the first date observed

                clean = medpath + str(afi) + '_fires_nodup.shp'
                arcpy.AddField_management(fires, "UID", "LONG", 10)
                r, rows = None, None

                rows = arcpy.UpdateCursor(fires)
                x = 1
                for r in rows:
                    r.UID = x
                    x += 1
                    rows.updateRow(r)

                del r, rows

                arcpy.CopyFeatures_management(fires, clean)
                desc = arcpy.Describe(fires)
                shapeFName = desc.ShapeFieldName

                rowsS = arcpy.SearchCursor(fires)
                uidList = []
                xList = []
                yList = []
                for row in rowsS:
                    uid = row.UID
                    uidList.append(uid)
                    feat = row.getValue(shapeFName)
                    p = feat.getPart()
                    x = p.X
                    y = p.Y
                    xList.append(x)
                    yList.append(y)

                del row, rowsS

                delUID = []

                for i in range(0, len(uidList)):
                    x = int(xList[i] / 100 + 0.5)
                    y = int(yList[i] / 100 + 0.5)

                    for k in range(i + 1, len(uidList)):
                        x1 = int(xList[k] / 100 + 0.5)
                        y1 = int(yList[k] / 100 + 0.5)
                        if x == x1 and y == y1:
                            delUID.append(uidList[k])

                set1 = set(delUID)
                delUIDn = list(set1)
                print 'original - ', len(uidList), 'removable - ', len(delUIDn), '\n'

                del set1, xList, yList, uidList, delUID
                print delUIDn

                if len(delUIDn) > 0:
                    tempLayer = arcpy.MakeFeatureLayer_management(clean, str(year) + 'clean_fire_')

                    for j in delUIDn:
                        expr4 = '"UID" = ' + str(j)
                        # print expr4
                        arcpy.SelectLayerByAttribute_management(tempLayer, "ADD_TO_SELECTION", expr4)

                    arcpy.DeleteRows_management(tempLayer)

                print 'Completed removal of residual burning from ' + str(year) + ' fires.\n'

except:
    # Get the traceback object
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    # Create message strings for python and arcpy tool
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
    # Add Python and ArcPy error messages to ArcGIS script too
    arcpy.AddError(pymsg)
    arcpy.AddError(msgs)
    # Print Python error messages in Python window
    print pymsg + "\n"
    print msgs

    print 'Program completed!'

