DEM_DIR="./" #"ftp.kortforsyningen.dk/dhm_danmarks_hoejdemodel/DTM/"
# Unzip all files in local FTP folder.
unzip $DEM_DIR'*.zip'

# Check md5sum for each file to ensure no corruption.
#   However, `md5sum -c DTM_1km_6049_684.md5` failes as the DEM md5 files is
#   wrongly formatted, as they are missing the file name after the checksum.
#   Thus we overwrite the md5sum files with the correct format.
FILES="*.md5"
for file_path in $FILES
do
    # Remove file extension to get file name.
    filename="${file_path%.*}"
    # Trim checksum file content - remove space and newlines.
    md5_checksum=`tr -d "[:space:]" < $file_path`
    # Overwrite each .md5 file with correct format.
    echo "$md5_checksum $filename.tif" > "$filename.md5"
done

echo "Checking md5 checksums:"
md5sum -c *.md5