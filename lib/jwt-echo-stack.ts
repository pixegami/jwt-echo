import { Stack, StackProps } from "aws-cdk-lib";
import { Construct } from "constructs";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as apiGateway from "aws-cdk-lib/aws-apigateway";
import { Code, Runtime } from "aws-cdk-lib/aws-lambda";

export class JwtEchoStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const apiFunction = new lambda.Function(this, "ApiFunction", {
      runtime: Runtime.PYTHON_3_9,
      code: Code.fromAsset("compute/lambda_function.zip"),
      handler: "main.handler",
    });

    const api = new apiGateway.LambdaRestApi(this, "ApiGateway", {
      handler: apiFunction,
    });

    api.root.addMethod("ANY");
    api.root.addCorsPreflight({
      allowOrigins: ["*"],
      allowHeaders: ["*"],
      allowMethods: ["ANY"],
    });
  }
}
