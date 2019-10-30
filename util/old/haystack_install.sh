curl -L -O https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.5.3.tar.gz
tar -xvf elasticsearch-5.5.3.tar.gz
cd elasticsearch-5.5.3/bin
./elasticsearch

pip install git+https://github.com/django-haystack/django-haystack
