# use curl to execute a smoke test -  post a request and display the result
# 
resp=$(curl  -H Content-Type:application/json -XPOST http://localhost:5080 -d '{"Foo": "Bar"}')
echo request was '{"Foo": "Bar"}' reply was $resp

