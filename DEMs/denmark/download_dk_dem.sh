# Load environment variables from `.env` file.
export $(grep -v '^#' ../../.env | xargs)

FTP_HOST="ftp://ftp.kortforsyningen.dk"
FTP_DIR="/dhm_danmarks_hoejdemodel/DTM/DTM_628_54_TIF_UTM32-ETRS89.zip"
LOCAL_DIR='./'

echo "Your are about to miror all data (!many GB!) from '$FTP_HOST$FTP_DIR' to '$PWD'"
read -p "Are you sure you want to miror all ? [y/n] " CONT
if [ "$CONT" = "y" ]; then
    # Mirror FTP folder to current local directory.
    wget -r --user=$KORTFORSYNING_USERNAME --password=$KORTFORSYNING_PASSWORD $FTP_HOST$FTP_DIR -P $LOCAL_DIR
else
  echo "Selected no - Exit";
fi
