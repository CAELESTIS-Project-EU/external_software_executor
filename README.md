# REST API for external software executor

This repository contains a REST API to execute external deployed software for the CAELESTIS Interoperable Simulation Ecosystem.

## API description

The API is very simple it just contain an endpoint to run a software

### Run software

#### Request

`POST /run`

```json
{
  "software": "software_name",
  "parameters":{
    "param_name": "param_value",
  }
}
```

#### Response

```
HTTP/1.1 201 Created

{
  "status": "success",
  "output": "output_message"
}
```

## Running the service

To deploy the service user just need to run the following command:

```bash
python3 app.py
```

## Configuring the API for an specific software

To configure the API to support a specific software user has to modify the `config/available_software.json` file. Users has to add a line with every supported software in the API specifying the command to run including the parameters.

``` json
{
   "software_name": "software_cmd {parameter_name}"
}
```

## Example

For instance, if you want to run the list a directory in linux you will define the `config/available_software.json` file as follows.

``` json
{
        "list" : "ls {flags} {dir}"
}
```

The endpoint can be invoked using cURL as follows

```bash
curl -X POST -H "Content-Type: application/json" \
   -d '{"software": "list", "parameters": {"flags": "-l", "dir": "/home/jorgee"} }' \
   http://127.0.0.1:5000/run
```
	
This work has been developed in the CAELESTIS project. This project has received funding from the European Union’s HORIZON research and innovation program under grant agreement nº 101056886
