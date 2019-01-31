DATE=`date +%Y-%m-%d`
mongodump --db critique_django --gzip --archive=/home/ria/tln/mongo_bkp/critique.$DATE.gz
