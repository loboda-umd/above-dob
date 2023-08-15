pro IDW_UID_extract

;extract out UID value for excel check

path = 'D:\ABoVE\Version2.0_2016_2019_update\Output\2018\IDW\clip\'

files = file_search(path + '*.shp')

for f = 0, n_elements(files)-1 do begin
  
  file = files[f]
  name = strsplit(file, '_',/extract)
  oname = name[4]
 print, oname
  
endfor

stop

end