# RxReader
Empowering patients with clear and accurate prescription (Rx) information.

To test the API you can use postman its hosted on 172.178.105.199 , Make a post call with endpoint as http://172.178.105.199:5000/prescriptiondetails and in body click form data type image as key and select prescription image as file (currently model works only for typed prescription not handwritten)


Curl Command:

curl --location 'http://172.178.105.199:5000/prescriptiondetails' \
--form 'image=@"/C:/Users/abhinagupta/Downloads/Testdata/IMG-6146Dup.jpg"




