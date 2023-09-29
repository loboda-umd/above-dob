pro FPM_Consecutive_Days

;This code reads in the yearly AF Scar Join Attribute Table
;Extract out all the gaps (over 20 days) in daily observations per scar
;You can alter this code to only extract out the scar ID

path = 'D:\Dropbox\ABOVE\Fire_progression\Version2.0_2016_2019_update\consecutive_testing\yearly\'

for year = 2016, 2019 do begin
  infile = strcompress(path+string(year)+'_FD_AF.csv',/remove_all)
  outfile = strcompress(path+string(year)+'_FD_AF_diff_20day.csv',/remove_all)
  data = read_csv(infile)
  
  
  YYYYMMDD = data.field06
  scar_UID = data.field20
  
  ;loop through the unique scar UID
  uniq_scar_list =scar_UID[uniq(scar_UID, SORT(scar_UID))]
  hy = size(uniq_scar_list,/dimensions)
  
  ;creating the final output array. It will hopefully be smaller than this array. If not, then create a larger array
  outarr = strarr(2, hy)
  x=0
  
  ;find the list of dates associated with each scar
  for i = 0, n_elements(uniq_scar_list)-1 do begin

    scar = uniq_scar_list[i]
    ;print, 'this is the scar ' +string(scar)

    date_list = YYYYMMDD[where(scar_UID eq scar, count)]
    ;print, date_list

    if count eq 0 then stop ; this is used during the testing phase
    
    ;;;;;sort the list and create a moving window of 10, 15, 20 days to find any instances of non-continous fires
    ;;;;;change date into JD
    date_array = intarr(count)
    z = 0
    for d = 0, n_elements(date_list)-1 do begin

      date = date_list[d]
      yr = strmid(date,4,4)
      mon = strmid(date,8,2)
      day = strmid(date,10,2)

      if yr ne year then stop
      if mon gt 12 then stop
      if day gt 31 then stop

      ;print, yr, mon, day
      JD = JULDAY( mon, day, yr ) - JULDAY( 1, 0, yr )
      ;print, JD
      date_array[z] = JD
      z = z +1
    endfor ; d - date list

    ;print, date_array

    ;;;;;;sort array by JD
    jd_sort_arr = date_array[sort(date_array)]
    jd_len = size(jd_sort, /dimensions)
    
    for j = 0,n_elements(jd_sort_arr)-2 do begin

      jd_sort2 = jd_sort_arr[j+1]
      jd_sort1 = jd_sort_arr[j]
      diff = jd_sort2 - jd_sort1
      ;print, diff

      if diff gt 20 then begin ; I am checking for a 20 day window
        out_name = strcompress(string(year)+'_'+string(scar), /remove_all)
        ;print, out_name
        outarr[0,x] = scar
        outarr[1,x] = diff

        x = x+1
      endif
    endfor ; j - jd sort array

  endfor; i - uniq scar list  
  write_csv, outfile, outarr
endfor; year

end