base='https://company.meralco.com.ph/news-and-advisories/rates-archives'
format=${base}'?field_downloadable_file_category_target_id_1=All&field_date_created_value=All&page='

# handle special case, latest rate archives
wget -O 0.html $base

# handle all other archives
# TODO: max of 88 found by manually trying the maximum valid query param for page, must be adjusted when new data is added
# for i in {1..88}
# do
# wget -O $i.html ${format}$i
# done

