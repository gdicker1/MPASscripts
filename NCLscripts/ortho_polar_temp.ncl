begin
    start_code = get_cpu_time()   

;---Set defaults for varname, if not provided on command line.
    if(.not.isvar("varname")) then
      varname = "surface_pressure"
    end if
    
    mpas_init_file = "x1.5898242.init.nc"
    fi = addfile(mpas_init_file,"r")
      
    latCell = fi->latCell
    lonCell = fi->lonCell
    RAD2DEG = get_r2d(typeof(lonCell))      ; Radian to Degree
    lonCell = lonCell*RAD2DEG
    latCell = latCell*RAD2DEG
    ncells  = dimsizes(latCell)

    latVertex = fi->latVertex
    lonVertex = fi->lonVertex
    RAD2DEG = get_r2d(typeof(lonVertex))      ; Radian to Degree
    lonVertex = lonVertex*RAD2DEG
    latVertex = latVertex*RAD2DEG
    nverts  = dimsizes(latVertex)
    centLon = 202.5
    iter=0
    do day=1,30
      do hr=0,23
        mpas_diag_file = "diag.0000-01-"+sprinti("%0.2i",day)+"_"+sprinti("%0.2i",hr)+".00.00.nc"
        fd = addfile(mpas_diag_file,"r")
    
        temp = fd->temperature_850hPa(0,:)     ; Grab first time step

        print("==================================================")
        print("Diag file  : " + mpas_diag_file)


    ;----------------- plot temp -----------------------------------
        wks_temp = gsn_open_wks("png","orthoSpin_jw2_56_temp_"+sprinti("%0.3i",iter))
        gsn_define_colormap(wks_temp,"TEMP")
        varname = "Temperature @ 850hPa"
        tres                       = True              ; Plot mods desired.

        tres@gsnMaximize           = True              ; Maximize plot
        tres@mpOutlineOn         = False
        tres@mpCenterLatF        = 45
        tres@mpCenterLonF        = centLon
        tres@mpProjection        = "Orthographic"
        tres@mpDataBaseVersion   = "LowRes"
        tres@mpGeophysicalLineColor = "black"
        tres@mpOutlineOn         = True
        tres@mpPerimOn           = False
        tres@mpFillOn            = False
        tres@mpGeophysicalLineThicknessF = 4.0
        tres@pmTickMarkDisplayMode = "Never"   ; better map tickmarks

        tres@cnFillOn              = True              ; color plot desired
        tres@cnFillMode            = "RasterFill"      ; USES LESS MEMORY AND IS FASTER
        tres@cnLinesOn             = True             ; turn off contour lines
        tres@cnLineLabelsOn        = False             ; turn off contour labels
        tres@cnConstFEnableFill    = True
        tres@lbBoxLinesOn          = False             ; turn off labelbar box lines
        tres@pmLabelBarWidthF      = 0.1               ; increase width of labelbar
        tres@cnMaxLevelCount       = 9                ; default is 16
        tres@cnLevelSelectionMode = "ManualLevels"       ; manually set the contour levels
        tres@cnMinLevelValF  = 230.                      ; set the minimum contour level
        tres@cnMaxLevelValF  = 300.                     ; set the maximum contour level
        tres@cnLevelSpacingF = 10.                        ; set the interval between contours
        tres@lbLabelStride         = 1
        tres@pmLabelBarWidthF      = .6
        tres@pmTitleZone           = 4                 ; move title down

        tres@mpFillOn              = False
        tres@pmTickMarkDisplayMode = "Never"          ; nicer map tickmark label
        tres@pmLabelBarOrthogonalPosF = .20            ; move whole thing downs

        tres@sfXArray              = lonCell           ; necessary for plotting MPAS
        tres@sfYArray              = latCell
        tres@gsnAddCyclic          = False

        tres@tiMainFontHeightF     = 0.02
         
        tres@tiMainString          = "Day: "+sprinti("%0.2i",day-1)+" Hr: "+sprinti("%0.2i",hr)+ " " + varname + ", " + ncells + " cells"
    
        plot = gsn_csm_contour_map(wks_temp,temp,tres)
        
        ;-----polar NH
        plotP = new(2,graphic)                          ; create a plot array

        wks = gsn_open_wks("png","polar_jw2_56_temp_"+sprinti("%0.3i",iter))            ; send graphics to PNG file
  	gsn_define_colormap(wks, "TEMP")

  	res            = True                         ; plot mods desired
  	res@gsnPolar   = "NH"                         ; specify the hemisphere
  	res@mpMinLatF  = 30                           ; minimum lat to plot
  	res@mpFillOn   = False

  	res@cnFillOn          = True                  ; color fill
  	res@cnLevelSpacingF   = 10.                    ; interval spacing
  	res@cnLinesOn         = True                 ; no contour lines
        res@cnMinLevelValF  = 230.                      ; set the minimum contour level
        res@cnMaxLevelValF  = 300.                     ; set the maximum contour level
        res@cnLevelSpacingF = 10.                        ; set the interval between contours
        res@lbLabelBarOn        = False 
        ;res@lbLabelStride         = 1
        ;res@pmLabelBarWidthF      = .6
        ;res@pmTitleZone           = 4                 ; move title down
 
        res@sfXArray              = lonCell           ; necessary for plotting MPAS
        res@sfYArray              = latCell
        res@gsnAddCyclic          = False
        res@gsnDraw  = False
        res@gsnFrame = False 
        ;res@tiMainFontHeightF     = 0.02

        ;res@tiMainString          = "Day: "+sprinti("%0.2i",day-1)+" Hr: "+sprinti("%0.2i",hr)+ " " + varname
        
        SHres            = True                         ; plot mods desired
        SHres@gsnPolar   = "SH"                         ; specify the hemisphere
        SHres@mpMinLatF  = -30                           ; minimum lat to plot
        SHres@mpFillOn   = False

        SHres@cnFillOn          = True                  ; color fill
        SHres@cnLevelSpacingF   = 10.                    ; interval spacing
        SHres@cnLinesOn         = True                 ; no contour lines
        SHres@cnMinLevelValF  = 230.                      ; set the minimum contour level
        SHres@cnMaxLevelValF  = 300.                     ; set the maximum contour level
        SHres@cnLevelSpacingF = 10.                        ; set the interval between contours
        SHres@lbLabelBarOn        = False
        SHres@gsnDraw  = False
        SHres@gsnFrame = False  
        ;SHres@lbLabelStride         = 1
        ;SHres@pmLabelBarWidthF      = .6
        ;res@pmTitleZone           = 4                 ; move title down

        SHres@sfXArray              = lonCell           ; necessary for plotting MPAS
        SHres@sfYArray              = latCell
        SHres@gsnAddCyclic          = False
 

        plotP(0) = gsn_csm_contour_map_polar(wks,temp,res)
        plotP(1) = gsn_csm_contour_map_polar(wks,temp,SHres)
       

        resP                     = True                ; modify the panel plot
        resP@gsnPanelMainString = "Day: "+sprinti("%0.2i",day-1)+" Hr: "+sprinti("%0.2i",hr)+ " " + varname

        resP@gsnPanelLabelBar    = True                ; add common colorbar
        res@lbLabelStride         = 1
        res@pmLabelBarWidthF      = .6
        res@pmTitleZone           = 4
        resP@lbLabelFontHeightF  = 0.007               ; make labels smaller

        gsn_panel(wks,plotP,(/2,1/),resP)               ; now draw as one plot
        centLon = centLon + -0.5
        iter = iter + 1
      end do
    end do
end
