import { Stack, StackProps } from "aws-cdk-lib";
import { Construct } from "constructs";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as apiGateway from "aws-cdk-lib/aws-apigateway";
import { Code, Runtime } from "aws-cdk-lib/aws-lambda";

export class JwtEchoStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    // Create common Lambda layer.
    const layer = new lambda.LayerVersion(this, "BaseLayer", {
      code: lambda.Code.fromAsset("compute/base_layer/layer.zip"),
      compatibleRuntimes: [lambda.Runtime.PYTHON_3_8],
      license: "Apache-2.0",
      description: "Python base layer with FastAPI.",
    });

    const apiFunction = new lambda.Function(this, "ApiFunction", {
      runtime: Runtime.PYTHON_3_8,
      code: Code.fromAsset("compute"),
      handler: "main.handler",
      layers: [layer],
    });

    const api = new apiGateway.LambdaRestApi(this, "ApiGateway", {
      handler: apiFunction,
      proxy: false,
    });

    api.root.addMethod("ANY");
    api.root.addCorsPreflight({
      allowOrigins: ["*"],
      allowHeaders: ["*"],
      allowMethods: ["ANY"],
    });
  }
}
