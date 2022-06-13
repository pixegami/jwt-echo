# JWT Echo

This is a simple API to echo back the JWT payload in the Authorization header.

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer XYZ'
```

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6Imluc18yQVFIRXdpbjNIbjU4T1RzS3daUGlsWkFTTkciLCJ0eXAiOiJKV1QifQ.eyJhenAiOiJodHRwOi8vbG9jYWxob3N0OjMwMDAiLCJleHAiOjE2NTUxMjI0NzgsImlhdCI6MTY1NTEyMjQxOCwiaXNzIjoiaHR0cHM6Ly9jbGVyay5hY3RpdmUuc2hyaW1wLTg1LmxjbC5kZXYiLCJuYmYiOjE2NTUxMjI0MDgsInNpZCI6InNlc3NfMkFXTFl2TUROOGwySlA4VDBPZkxyVFRadGNoIiwic3ViIjoidXNlcl8yQVFJdk5WaUsyejhxUTJObGptcXZia2pUbDcifQ.c74KQiNJjm8Le32o-i9w3n3svPfMjY0zvMBs2HDugwCInIjXdWK6d-1ihtk0cb550Pyl0RE24XLPCtKyDEcx9XMggXaOQiAZj2jPcrw1Ul-igCTadiGcq8qXW8JHTp6hH_Bi_y2hlsyHzRf1PEpYVGGld3CqzLTjhkrrWD6f-X-aQY_sGO1ElB0I9rBnB4Atoi2qCTN9cE79qyodUXnEQBRhM3K6_mqJxbmnPiOKouSwbo__dlXlZ6dz1dWqZjQfaW36viEj4rMTCKsUG3pQnxpZ4WfxE37TwQ1YL6Mmw5WgkGd2GcQc5da_3Cd4DjLXqgm4bwaQqDHstdn4uH0ZUw'
```
### Compute Artifacts

We'll also need to install the dependencies into a local directory so we can zip it up.

```bash
pip install -t lib -r requirements.txt
```

We now need to zip it up.

```
(cd lib; zip ../lambda_function.zip -r .)
```

Now add our FastAPI file and the JSON file.

```
zip lambda_function.zip -u main.py
zip lambda_function.zip -u books.json
```


# Welcome to your CDK TypeScript project

This is a blank project for CDK development with TypeScript.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

## Useful commands

* `npm run build`   compile typescript to js
* `npm run watch`   watch for changes and compile
* `npm run test`    perform the jest unit tests
* `cdk deploy`      deploy this stack to your default AWS account/region
* `cdk diff`        compare deployed stack with current state
* `cdk synth`       emits the synthesized CloudFormation template
