# from google.cloud import bigquery

# # Construct a BigQuery client object.
# client = bigquery.Client()

# table_id = 'businessintelligence-320707.Customer_Service.3cx'
# rows_iter = client.list_rows(table_id)
# # for i in rows_iter:
# #     print(i)

# print(rows_iter)


# rows_to_insert = [
#     {u"full_name": u"Phred Phlyntstone", u"age": 32},
#     {u"full_name": u"Wylma Phlyntstone", u"age": 29},
# ]

# errors = client.insert_rows_json(table_id, rows_to_insert)  # Make an API request.
# if errors == []:
#     print("New rows have been added.")
# else:
#     print("Encountered errors while inserting rows: {}".format(errors))
