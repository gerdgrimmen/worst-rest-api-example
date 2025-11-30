# worst REST API example

Minimal REST API example

## Description

This is Project is build on: https://github.com/ynsrc/python-simple-rest-api/tree/main
All Credits go to that Project.

This Project only adds a "http delete" to the existing post and get. The data is not persisted in this main.py.
Also changes the approach to have multiple object endpoints by changing the method instead of the path.

### Dependencies

* import json
* from http.server import HTTPServer, BaseHTTPRequestHandler
* from urllib.parse import urlparse, parse_qs

### Installing

* Downloading/Copying the script

### Executing program

just run the command "python ./main.py"

```
python ./main.py
```
To use the API just take the examples from the ./curls.sh.

You can edit the endpoint by adjusting the term "data" to your needs:
* in the api_data dict
* endpoints:  @api.get("/data") , @api.post("/data") etc.
* and editing the access of the dict object: api_data["data"]

## Authors

Contributors names and contact info

ex. Gerd Grimmen (F.KU)

## Version History
* 0.3.0
    * change POST, GET processing
    * add 40x return code responsemethods
    * add single dataset endpoint with "/<id>" syntacs
* 0.2.2
    * change License due to lack of acknowledgement for "Unlicense" in Germany
    * License from this version on is CC0 1.0
* 0.2.1
    * fix image output as result - don't know, why I deleted that part before committing
* 0.2
    * Added PUT Method (Takes in binary data, for now planned for images)
    * can also give a respone with a returned string intead of a dict. Now it can handle requests for static sites or text elements  
* 0.1
    * Nothing here to see

## License

This work is marked CC0 1.0. To view a copy of this mark, visit https://creativecommons.org/publicdomain/zero/1.0/


## Acknowledgments

* https://github.com/ynsrc/python-simple-rest-api/tree/main