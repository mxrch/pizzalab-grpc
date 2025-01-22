Remove-Item pizzalab\grpc\* -Confirm:$false -Force -Recurse
$protos = Get-ChildItem .\protos\*.proto -Name
poetry run python -m grpc_tools.protoc -I ./protos --python_betterproto_out=./pizzalab/grpc $protos