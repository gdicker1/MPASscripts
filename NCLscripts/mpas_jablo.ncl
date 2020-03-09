begin
    start_code = get_cpu_time()   

;---Set defaults for varname, if not provided on command line.
    if(.not.isvar("varname")) then
      varname = "surface_pressure"
    end if
    
    mpas_init_file = "x1.655362.init.nc"
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

    iter=0
    do day=1,31
      do hr=0,23,2
        ;mpas_init_file = "x1.655362.init.nc"
        mpas_hist_file = "history.0000-01-"+sprinti("%0.2i",day)+"_"+sprinti("%0.2i",hr)+".00.00.nc"
        mpas_diag_file = "diag.0000-01-"+sprinti("%0.2i",day)+"_"+sprinti("%0.2i",hr)+".00.00.nc"
        fh = addfile(mpas_hist_file,"r")
        fd = addfile(mpas_diag_file,"r")

        cf1 = fh->cf1
        cf2 = fh->cf2
        cf3 = fh->cf3
        h0= (fh->pressure_p(0,:,0) + fh->pressure_base(0,:,0))/100.
        h1= (fh->pressure_p(0,:,1) + fh->pressure_base(0,:,1))/100.
        h2= (fh->pressure_p(0,:,2) + fh->pressure_base(0,:,2))/100.
        sp = (cf1*h0 + cf2*h1 + cf3*h2)
        sp@units = "hPa"

        rv = fd->vorticity_850hPa(0,:)     ; Grab first time step
        rv = rv*10000
        rv@units = "10^-5 s^-1" 
    
        temp = fd->temperature_850hPa(0,:)     ; Grab first time step

;---Print some information, look at your data!
        print("==================================================")
        print("Diag file  : " + mpas_diag_file)

;---Start the graphics
        varname = "surface_pressure"

        wks_sp = gsn_open_wks("png","jw2_56_cm_mpas_sp_"+sprinti("%0.3i",iter))
        gsn_define_colormap(wks_sp,"SP2")
        res                       = True              ; Plot mods desired.

        res@gsnMaximize           = True              ; Maximize plot
        res@mpOutlineOn         = False
        res@mpMinLonF           = 45
        res@mpMaxLonF           = 360
        res@mpMinLatF           = 0
        res@mpMaxLatF           = 90
        res@mpCenterLonF        = 202.5
        res@pmTickMarkDisplayMode = "Always"   ; better map tickmarks

        res@cnFillOn              = True              ; color plot desired
        res@cnFillMode            = "RasterFill"      ; USES LESS MEMORY AND IS FASTER
        ;res@cnFillPalette         = "CBR_coldhot"     ;"cmp_b2r"         ;"gscyclic"        ;"BlGrYeOrReVi200"
        res@cnLinesOn             = True             ; turn off contour lines
        res@cnLineLabelsOn        = False             ; turn off contour labels
        res@cnConstFEnableFill    = True
        res@lbBoxLinesOn          = False             ; turn off labelbar box lines
        res@pmLabelBarWidthF      = 0.1               ; increase width of labelbar
        res@cnMaxLevelCount       = 9                ; default is 16
        res@cnLevelSelectionMode = "ManualLevels"	; manually set the contour levels 
        res@cnMinLevelValF  = 940.			; set the minimum contour level
        res@cnMaxLevelValF  = 1020.			; set the maximum contour level
        res@cnLevelSpacingF = 10.			; set the interval between contours
        res@lbLabelStride         = 2
        res@pmLabelBarWidthF      = .6
        res@pmTitleZone           = 4                 ; move title down

        res@mpFillOn              = False
        res@pmTickMarkDisplayMode = "Always"          ; nicer map tickmark label
        res@pmLabelBarOrthogonalPosF = .20            ; move whole thing downs

        res@sfXArray              = lonCell           ; necessary for plotting MPAS
        res@sfYArray              = latCell
        res@gsnAddCyclic          = False

        res@tiMainString          = "Day: "+sprinti("%0.2i",day)+" Hr: "+sprinti("%0.2i",hr)+ " " + varname + ", " + ncells + " cells"
        res@tiMainFontHeightF     = 0.02

        plot = gsn_csm_contour_map(wks_sp,sp,res) 


    ;-----------------plot sp2 ------------------------------------

        wks_sp2 = gsn_open_wks("png","jw2_56_cm_mpas_sp2_"+sprinti("%0.3i",iter))
        gsn_define_colormap(wks_sp2,"SP1")
        sp2res                       = True              ; Plot mods desired.

        sp2res@gsnMaximize           = True              ; Maximize plot
        sp2res@mpOutlineOn         = False
        sp2res@mpMinLonF           = 45
        sp2res@mpMaxLonF           = 360
        sp2res@mpMinLatF           = 0
        sp2res@mpMaxLatF           = 90
        sp2res@mpCenterLonF        = 202.5
        sp2res@pmTickMarkDisplayMode = "Always"   ; better map tickmarks

        sp2res@cnFillOn              = True              ; color plot desired
        sp2res@cnFillMode            = "RasterFill"      ; USES LESS MEMORY AND IS FASTER
        ;sp2res@cnFillPalette         = "CBR_coldhot"     ;"cmp_b2r"         ;"gscyclic"        ;"BlGrYeOrReVi200"
        sp2res@cnLinesOn             = True             ; turn off contour lines
        sp2res@cnLineLabelsOn        = False             ; turn off contour labels
        sp2res@cnConstFEnableFill    = True
        sp2res@lbBoxLinesOn          = False             ; turn off labelbar box lines
        sp2res@pmLabelBarWidthF      = 0.1               ; increase width of labelbar
        sp2res@cnMaxLevelCount       = 6                 ; default is 16
        sp2res@cnLevelSelectionMode = "ManualLevels"       ; manually set the contour levels
        sp2res@cnMinLevelValF  = 994.                      ; set the minimum contour level
        sp2res@cnMaxLevelValF  = 1004.                     ; set the maximum contour level
        sp2res@cnLevelSpacingF = 2.                        ; set the interval between contours
        sp2res@lbLabelStride         = 2
        sp2res@pmLabelBarWidthF      = .6
        sp2res@pmTitleZone           = 4                 ; move title down

        sp2res@mpFillOn              = False
        sp2res@pmTickMarkDisplayMode = "Always"          ; nicer map tickmark label
        sp2res@pmLabelBarOrthogonalPosF = .20            ; move whole thing downs

        sp2res@sfXArray              = lonCell           ; necessary for plotting MPAS
        sp2res@sfYArray              = latCell
        sp2res@gsnAddCyclic          = False

        sp2res@tiMainString          = "Day: "+sprinti("%0.2i",day)+" Hr: "+sprinti("%0.2i",hr)+ " " + varname + ", " + ncells + " cells"
        sp2res@tiMainFontHeightF     = 0.02

        plot = gsn_csm_contour_map(wks_sp2,sp,sp2res)

    ;----------------- plot temp -----------------------------------
        ;wks_temp = gsn_open_wks("png","jw2_mpas_temp_"+sprinti("%0.2i",day)+"_"+sprinti("%0.2i",hr))
        wks_temp = gsn_open_wks("png","jw2_56_cm_mpas_temp_"+sprinti("%0.3i",iter))
        gsn_define_colormap(wks_temp,"TEMP")
        varname = "temp_850hPa"
        tres                       = True              ; Plot mods desired.

        tres@gsnMaximize           = True              ; Maximize plot
        tres@mpOutlineOn         = False
        tres@mpMinLonF           = 45
        tres@mpMaxLonF           = 360
        tres@mpMinLatF           = 0
        tres@mpMaxLatF           = 90
        tres@mpCenterLonF        = 202.5
        tres@pmTickMarkDisplayMode = "Always"   ; better map tickmarks

        tres@cnFillOn              = True              ; color plot desired
        tres@cnFillMode            = "RasterFill"      ; USES LESS MEMORY AND IS FASTER
        ;tres@cnFillPalette         = "CBR_coldhot"         ;"gscyclic"        ;"BlGrYeOrReVi200"
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
        tres@pmTickMarkDisplayMode = "Always"          ; nicer map tickmark label
        tres@pmLabelBarOrthogonalPosF = .20            ; move whole thing downs

        tres@sfXArray              = lonCell           ; necessary for plotting MPAS
        tres@sfYArray              = latCell
        tres@gsnAddCyclic          = False

        tres@tiMainFontHeightF     = 0.02
         
        tres@tiMainString          = "Day: "+sprinti("%0.2i",day)+" Hr: "+sprinti("%0.2i",hr)+ " " + varname + ", " + ncells + " cells"
    
        plot = gsn_csm_contour_map(wks_temp,temp,tres)

    ;---------------- plot relative vort ---------------------------
        ;wks_rv = gsn_open_wks("png","jw2_mpas_rv_"+sprinti("%0.2i",day)+"_"+sprinti("%0.2i",hr))
        wks_rv = gsn_open_wks("png","jw2_56_cm_mpas_rv_"+sprinti("%0.3i",iter))
        gsn_define_colormap(wks_rv,"RV1")
        varname = "relative vorticity_850hPa"

        res_rv                       = True              ; Plot mods desired.

        res_rv@gsnMaximize           = True              ; Maximize plot
        res_rv@mpOutlineOn         = False
        res_rv@mpMinLonF           = 90
        res_rv@mpMaxLonF           = 210
        res_rv@mpMinLatF           = 25
        res_rv@mpMaxLatF           = 75
        res_rv@mpCenterLonF        = 150
        res_rv@pmTickMarkDisplayMode = "Always"   ; better map tickmarks

        res_rv@cnFillOn              = True              ; color plot desired
        res_rv@cnFillMode            = "RasterFill"      ; USES LESS MEMORY AND IS FASTER
        ;res_rv@cnFillPalette         = "CBR_coldhot"     ;"cmp_b2r" "gscyclic" "BlGrYeOrReVi200"
        res_rv@cnLinesOn             = True             ; turn off contour lines
        res_rv@cnLineLabelsOn        = False             ; turn off contour labels
        res_rv@lbBoxLinesOn          = False             ; turn off labelbar box lines
        res_rv@pmLabelBarWidthF      = 0.1               ; increase width of labelbar
        res_rv@cnMaxLevelCount       = 8                ; default is 16
        res_rv@cnLevelSelectionMode = "ManualLevels"   ; manually set the contour levels
        res_rv@cnMinLevelValF  = -2.                   ; set the minimum contour level
        res_rv@cnMaxLevelValF  = 5.                    ; set the maximum contour level
        res_rv@cnLevelSpacingF = 1.                    ; set the interval between contours
        res_rv@cnConstFEnableFill    = True
        res_rv@lbLabelStride         = 1
        res_rv@pmLabelBarWidthF      = .6
        res_rv@pmTitleZone           = 4                 ; move title down

        res_rv@mpFillOn              = False
        res_rv@pmTickMarkDisplayMode = "Always"          ; nicer map tickmark label
        res_rv@pmLabelBarOrthogonalPosF = .20            ; move whole thing downs

        res_rv@sfXArray              = lonVertex           ; necessary for plotting MPAS
        res_rv@sfYArray              = latVertex
        res_rv@gsnAddCyclic          = False

        res_rv@tiMainString          = "Day: "+sprinti("%0.2i",day)+" Hr: "+sprinti("%0.2i",hr)+ " "+ varname + ", " + nverts + " vertices"
        plot = gsn_csm_contour_map(wks_rv,rv,res_rv)

        ;------------------------- plot rv2 ------------------------
        wks_rv2 = gsn_open_wks("png","jw2_56_cm_mpas_rv2_"+sprinti("%0.3i",iter))
        gsn_define_colormap(wks_rv2,"RV2")
        varname = "relative vorticity_850hPa"

        res_rv2                       = True              ; Plot mods desired.

        res_rv2@gsnMaximize           = True              ; Maximize plot
        res_rv2@mpOutlineOn         = False
        res_rv2@mpMinLonF           = 120
        res_rv2@mpMaxLonF           = 270
        res_rv2@mpMinLatF           = 25
        res_rv2@mpMaxLatF           = 75
        res_rv2@mpCenterLonF        = 195
        res_rv2@pmTickMarkDisplayMode = "Always"   ; better map tickmarks

        res_rv2@cnFillOn              = True              ; color plot desired
        res_rv2@cnFillMode            = "RasterFill"      ; USES LESS MEMORY AND IS FASTER
        ;res_rv2@cnFillPalette         = "CBR_coldhot"     ;"cmp_b2r" "gscyclic" "BlGrYeOrReVi200"
        res_rv2@cnLinesOn             = True             ; turn off contour lines
        res_rv2@cnLineLabelsOn        = False             ; turn off contour labels
        res_rv2@lbBoxLinesOn          = False             ; turn off labelbar box lines
        res_rv2@pmLabelBarWidthF      = 0.1               ; increase width of labelbar
        res_rv2@cnMaxLevelCount       = 9                ; default is 16
        res_rv2@cnLevelSelectionMode = "ManualLevels"   ; manually set the contour levels
        res_rv2@cnMinLevelValF  = -5.                   ; set the minimum contour level
        res_rv2@cnMaxLevelValF  = 35.                    ; set the maximum contour level
        res_rv2@cnLevelSpacingF = 5.                    ; set the interval between contours
        res_rv2@cnConstFEnableFill    = True
        res_rv2@lbLabelStride         = 1
        res_rv2@pmLabelBarWidthF      = .6
        res_rv2@pmTitleZone           = 4                 ; move title down

        res_rv2@mpFillOn              = False
        res_rv2@pmTickMarkDisplayMode = "Always"          ; nicer map tickmark label
        res_rv2@pmLabelBarOrthogonalPosF = .20            ; move whole thing downs

        res_rv2@sfXArray              = lonVertex           ; necessary for plotting MPAS
        res_rv2@sfYArray              = latVertex
        res_rv2@gsnAddCyclic          = False

        res_rv2@tiMainString          = "Day: "+sprinti("%0.2i",day)+" Hr: "+sprinti("%0.2i",hr)+ " "+ varname + ", " + nverts + " vertices"
        plot = gsn_csm_contour_map(wks_rv2,rv,res_rv2)
        
        iter = iter + 1
      end do
    end do
end
