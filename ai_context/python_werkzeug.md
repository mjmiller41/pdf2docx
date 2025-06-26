TITLE: Creating a Simple Werkzeug WSGI Application (Python)
DESCRIPTION: This snippet demonstrates how to create a minimal 'Hello, World' web application using Werkzeug. It defines a simple WSGI application function wrapped with `@Request.application` to handle request/response cycles and uses `run_simple` to start a local development server.
SOURCE: https://github.com/pallets/werkzeug/blob/main/README.md#_snippet_0

LANGUAGE: Python
CODE:
```
# save this as app.py
from werkzeug.wrappers import Request, Response

@Request.application
def application(request: Request) -> Response:
    return Response("Hello, World!")

if __name__ == "__main__":
    from werkzeug.serving import run_simple
    run_simple("127.0.0.1", 5000, application)
```

----------------------------------------

TITLE: Installing Werkzeug with pip (sh)
DESCRIPTION: This command uses the `pip` package installer, which is available within the activated virtual environment, to download and install the Werkzeug library and its dependencies from the Python Package Index (PyPI). This should be run after activating the desired environment.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/installation.rst#_snippet_4

LANGUAGE: sh
CODE:
```
pip install Werkzeug
```

----------------------------------------

TITLE: WSGI Application using Werkzeug Response Python
DESCRIPTION: Shows how to implement a WSGI application using Werkzeug's `Response` object. Instead of manually calling `start_response`, the application creates a `Response` object, potentially modifies it, and then calls the response object itself with the environ and start_response arguments. This is the recommended pattern in Werkzeug.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/quickstart.rst#_snippet_16

LANGUAGE: Python
CODE:
```
from werkzeug.wrappers import Response

def application(environ, start_response):
    response = Response('Hello World!')
    return response(environ, start_response)
```

----------------------------------------

TITLE: Wrapping WSGI Environment with Request Object Python
DESCRIPTION: Shows how to create a `Request` object from an existing WSGI environment dictionary. The Request object provides a more convenient and high-level interface for accessing request data, handling decoding and parsing automatically. This is the standard way to interact with request data in Werkzeug.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/quickstart.rst#_snippet_2

LANGUAGE: Python
CODE:
```
from werkzeug.wrappers import Request
request = Request(environ)
```

----------------------------------------

TITLE: Starting Werkzeug Development Server (Python)
DESCRIPTION: Shows the basic usage of `werkzeug.serving.run_simple` to launch a local development server for a WSGI application. It demonstrates how to import the function and an application factory, create an application instance, and run the server on a specified host and port with the reloader enabled.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/serving.rst#_snippet_0

LANGUAGE: python
CODE:
```
from werkzeug.serving import run_simple
from myproject import make_app

app = make_app(...)
run_simple('localhost', 8080, app, use_reloader=True)
```

----------------------------------------

TITLE: Dispatching Requests with Werkzeug URL Adapter in Python
DESCRIPTION: This Python method demonstrates how to dispatch incoming requests to the appropriate handler function based on URL routing. It binds the URL map to the current request environment, matches the URL to find the endpoint and arguments, and then calls a corresponding instance method (prefixed with 'on_') passing the request and URL arguments.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/tutorial.rst#_snippet_12

LANGUAGE: python
CODE:
```
def dispatch_request(self, request):
    adapter = self.url_map.bind_to_environ(request.environ)
    try:
        endpoint, values = adapter.match()
        return getattr(self, f'on_{endpoint}')(request, **values)
    except HTTPException as e:
        return e
```

----------------------------------------

TITLE: Accessing Request HTTP Method Python
DESCRIPTION: Shows how to retrieve the HTTP method used for the request from the `Request` object's `method` attribute. This provides a standard way to check if the request was a GET, POST, PUT, etc. The snippet accesses `request.method` on a Request created from a default environ.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/quickstart.rst#_snippet_4

LANGUAGE: Python
CODE:
```
request.method
```

----------------------------------------

TITLE: Defining and Matching Werkzeug URL Rules in WSGI
DESCRIPTION: This snippet demonstrates how to create a Werkzeug `Map` object with a list of `Rule` instances defining various URL patterns and their corresponding endpoints. It then shows how to bind this map to a WSGI `environ` using `bind_to_environ` to get a `MapAdapter`, and use the `match()` method to find the matching endpoint and arguments for a given request path, handling potential routing exceptions like `NotFound` or `RequestRedirect` within a basic WSGI application structure.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/routing.rst#_snippet_0

LANGUAGE: Python
CODE:
```
    from werkzeug.routing import Map, Rule, NotFound, RequestRedirect
    from werkzeug.exceptions import HTTPException

    url_map = Map([
        Rule('/', endpoint='blog/index'),
        Rule('/<int:year>/', endpoint='blog/archive'),
        Rule('/<int:year>/<int:month>/', endpoint='blog/archive'),
        Rule('/<int:year>/<int:month>/<int:day>/', endpoint='blog/archive'),
        Rule('/<int:year>/<int:month>/<int:day>/<slug>',
             endpoint='blog/show_post'),
        Rule('/about', endpoint='blog/about_me'),
        Rule('/feeds/', endpoint='blog/feeds'),
        Rule('/feeds/<feed_name>.rss', endpoint='blog/show_feed')
    ])

    def application(environ, start_response):
        urls = url_map.bind_to_environ(environ)
        try:
            endpoint, args = urls.match()
        except HTTPException as e:
            return e(environ, start_response)
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [f'Rule points to {endpoint!r} with arguments {args!r}'.encode()]
```

----------------------------------------

TITLE: Accessing Request Object Attributes Python
DESCRIPTION: Demonstrates accessing common request attributes like path, script root, host, and URL directly from the `Request` object. These attributes parse and decode data from the underlying WSGI environment, offering easier usage compared to accessing the environ dict directly. The snippet retrieves `request.path`, `request.script_root`, `request.host`, and `request.url`.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/quickstart.rst#_snippet_3

LANGUAGE: Python
CODE:
```
request.path
request.script_root
request.host
request.url
```

----------------------------------------

TITLE: Accessing Request URL Arguments Python
DESCRIPTION: Illustrates how to access URL arguments (query string parameters) using the `request.args` attribute, which behaves like a dictionary. This provides easy access to parsed and decoded query parameters. The snippet shows retrieving the keys and a specific value from `request.args`.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/quickstart.rst#_snippet_7

LANGUAGE: Python
CODE:
```
request.args.keys()
request.args['blah']
```

----------------------------------------

TITLE: Defining URL Routing Map with Werkzeug - Python
DESCRIPTION: This code snippet, intended for the __init__ method of the Shortly class, creates a Werkzeug Map object with three routing Rules. These rules define how incoming URLs ('/', '/<short_id>', '/<short_id>+') are matched and mapped to specific endpoints, which will later be handled by corresponding methods.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/tutorial.rst#_snippet_11

LANGUAGE: python
CODE:
```
self.url_map = Map([
    Rule('/', endpoint='new_url'),
    Rule('/<short_id>', endpoint='follow_short_link'),
    Rule('/<short_id>+', endpoint='short_link_details')
])
```

----------------------------------------

TITLE: WSGI Application with Request Decorator Python
DESCRIPTION: Shows a more concise way to create a WSGI application using the `@Request.application` decorator provided by Werkzeug. This decorator simplifies application structure by handling the `environ` and `start_response` details internally and passing a ready-to-use `Request` object directly to the decorated function. The function then simply returns a `Response` object.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/wrappers.rst#_snippet_2

LANGUAGE: python
CODE:
```
from werkzeug.wrappers import Request, Response

@Request.application
def application(request):
    return Response(f"Hello {request.args.get('name', 'World!')}!")
```

----------------------------------------

TITLE: Creating Virtual Environment with venv (sh)
DESCRIPTION: This command sequence creates a project directory, navigates into it, and then uses Python's built-in `venv` module to create a virtual environment named 'venv' within the current directory. This is the standard method recommended for Unix-like systems.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/installation.rst#_snippet_0

LANGUAGE: sh
CODE:
```
mkdir myproject
cd myproject
python3 -m venv venv
```

----------------------------------------

TITLE: Running Werkzeug Development Server - Python
DESCRIPTION: This block runs the Werkzeug development server when the script is executed directly. It uses run_simple to serve the application, enabling the debugger and auto-reloader for development convenience. The server listens on 127.0.0.1:5000.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/tutorial.rst#_snippet_8

LANGUAGE: python
CODE:
```
if __name__ == '__main__':
    from werkzeug.serving import run_simple
    app = create_app()
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)
```

----------------------------------------

TITLE: Creating WSGI Entry Point (Python)
DESCRIPTION: Provides a Python snippet intended for a file like `wsgi.py` that imports an application factory function (`create_app`) and calls it to create the application object, making it available for uWSGI to import.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/deployment/uwsgi.rst#_snippet_3

LANGUAGE: python
CODE:
```
from hello import create_app

app = create_app()
```

----------------------------------------

TITLE: Activating Virtual Environment (bat)
DESCRIPTION: This command executes the activation script located within the 'venv' directory's 'Scripts' folder. Activating the environment modifies the Windows command prompt's environment variables to use the Python and packages installed within the virtual environment.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/installation.rst#_snippet_3

LANGUAGE: bat
CODE:
```
venv\Scripts\activate
```

----------------------------------------

TITLE: Making a Basic GET Request Werkzeug Test Client Python
DESCRIPTION: This snippet shows the fundamental usage of the `werkzeug.test.Client`. It demonstrates how to instantiate the client with a WSGI application, make a GET request to the root path, and then access key attributes of the response object, such as status code, headers, and body data.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/test.rst#_snippet_0

LANGUAGE: python
CODE:
```
>>> from werkzeug.test import Client
>>> from werkzeug.testapp import test_app
>>> c = Client(test_app)
>>> response = c.get("/")
>>> response.status_code
200
>>> response.headers
Headers([('Content-Type', 'text/html; charset=utf-8'), ('Content-Length', '5211')])
>>> response.get_data(as_text=True)
'<!doctype html>...'
```

----------------------------------------

TITLE: Accessing and Modifying Response Headers and Data Python
DESCRIPTION: Shows how to access and modify response headers via the `response.headers` attribute (a dictionary-like object) and access the response body via `response.data`. The snippet demonstrates getting the default 'content-type', accessing the data, and setting the 'content-length' header based on the data length. Headers are case-insensitive.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/quickstart.rst#_snippet_18

LANGUAGE: Python
CODE:
```
response.headers['content-type']
response.data
response.headers['content-length'] = len(response.data)
```

----------------------------------------

TITLE: Defining and Using LocalProxy for Request - Python
DESCRIPTION: This snippet demonstrates how to use `LocalProxy` to create a thread-safe, context-local variable representing the current request. A `ContextVar` named `_request_var` stores the actual request object, and the `request` `LocalProxy` allows functions like `check_auth` to access it directly as if it were the request object itself. This pattern avoids passing the request explicitly through the call stack and ensures each worker accesses its own request data. Requires `contextvars`, `werkzeug.local`, `werkzeug.wrappers`, and `werkzeug.exceptions`.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/local.rst#_snippet_0

LANGUAGE: python
CODE:
```
from contextvars import ContextVar
from werkzeug.local import LocalProxy

_request_var = ContextVar("request")
request = LocalProxy(_request_var)

from werkzeug.wrappers import Request

@Request.application
def app(r):
    _request_var.set(r)
    check_auth()
    ...

from werkzeug.exceptions import Unauthorized

def check_auth():
    if request.form["username"] != "admin":
        raise Unauthorized()
```

----------------------------------------

TITLE: Handling Missing Form Data Werkzeug Python
DESCRIPTION: This Python function demonstrates a common pattern in Werkzeug web applications where accessing `request.form` keys directly relies on special exceptions (like BadRequestKeyError) to handle missing data. If keys are missing, a BadRequest is raised automatically, simplifying view logic. Dependencies include Werkzeug's request object and potentially a `Post` model and `redirect` function.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/exceptions.rst#_snippet_0

LANGUAGE: python
CODE:
```
def new_post(request):
    post = Post(title=request.form['title'], body=request.form['body'])
    post.save()
    return redirect(post.url)
```

----------------------------------------

TITLE: Creating Request from Values for Testing Python
DESCRIPTION: Explains how to create a `Request` object directly from supplied data like query strings, form data (via `input_stream`), content type, and method, primarily for testing purposes using `Request.from_values`. This avoids needing a full WSGI environment setup to simulate specific request scenarios. The snippet simulates a POST request with a query string and form data payload.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/quickstart.rst#_snippet_5

LANGUAGE: Python
CODE:
```
from io import StringIO
data = "name=this+is+encoded+form+data&another_key=another+one"
request = Request.from_values(query_string='foo=bar&blah=blafasel',
    content_length=len(data), input_stream=StringIO(data),
    content_type='application/x-www-form-urlencoded',
    method='POST')
```

----------------------------------------

TITLE: Configuring Apache Reverse Proxy to WSGI (Apache)
DESCRIPTION: Sets up Apache httpd as a reverse proxy, loading necessary modules (`mod_proxy`, `mod_proxy_http`) to forward incoming requests (`/`) to a backend WSGI server running at `http://127.0.0.1:8000`. It also adds `X-Forwarded-Proto` and `X-Forwarded-Prefix` headers for the backend application, which should use `proxy_fix`.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/deployment/apache-httpd.rst#_snippet_1

LANGUAGE: apache
CODE:
```
LoadModule proxy_module modules/mod_proxy.so
LoadModule proxy_http_module modules/mod_proxy_http.so
ProxyPass / http://127.0.0.1:8000/
RequestHeader set X-Forwarded-Proto http
RequestHeader set X-Forwarded-Prefix /
```

----------------------------------------

TITLE: Applying ProxyFix Middleware to Werkzeug App (Python)
DESCRIPTION: This snippet demonstrates how to wrap a Werkzeug WSGI application (`app.wsgi_app`) with the `ProxyFix` middleware. It configures the middleware to trust one hop for the `X-Forwarded-For`, `X-Forwarded-Proto`, `X-Forwarded-Host`, and `X-Forwarded-Prefix` headers, allowing the application to see the client's real address and protocol instead of the proxy's. This is necessary when running the application behind a reverse proxy.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/deployment/proxy_fix.rst#_snippet_0

LANGUAGE: Python
CODE:
```
from werkzeug.middleware.proxy_fix import ProxyFix

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)
```

----------------------------------------

TITLE: Running Gunicorn with Module/Factory (Shell)
DESCRIPTION: Shows basic Gunicorn commands to start the server with 4 worker processes. It demonstrates how to specify the application entry point using either a module variable (`hello:app`) or a factory function call (`hello:create_app()`).
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/deployment/gunicorn.rst#_snippet_1

LANGUAGE: text
CODE:
```
# equivalent to 'from hello import app'
gunicorn -w 4 'hello:app'

# equivalent to 'from hello import create_app; create_app()'
gunicorn -w 4 'hello:create_app()'
```

----------------------------------------

TITLE: Sending Form Data with File Upload Werkzeug Test Client Python
DESCRIPTION: This example illustrates how to post data that includes both standard form fields and file uploads using the `client.post` method. Passing a dictionary to the `data` parameter allows specifying fields and files, where a file is represented by a tuple containing the file-like object (like `BytesIO`) and its filename. The client automatically sets the `Content-Type` header to `multipart/form-data` when files are included.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/test.rst#_snippet_1

LANGUAGE: python
CODE:
```
import io

response = client.post(data={
    "name": "test",
    "file": (io.BytesIO("file contents".encode("utf8")), "test.txt")
})
```

----------------------------------------

TITLE: Creating Response Object Python
DESCRIPTION: Demonstrates the basic creation of a `Response` object with a simple string body. The Response object encapsulates the HTTP response data, headers, and status code, providing a mutable interface for building the response. This snippet initializes a response with the body 'Hello World!'.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/quickstart.rst#_snippet_17

LANGUAGE: Python
CODE:
```
from werkzeug.wrappers import Response
response = Response("Hello World!")
```

----------------------------------------

TITLE: Accessing Request Form Data Python
DESCRIPTION: Demonstrates how to access form data submitted in the request body (e.g., from a POST request with `application/x-www-form-urlencoded` or `multipart/form-data`) using the `request.form` attribute. This also behaves like a dictionary, providing parsed and decoded form values. The snippet retrieves a value from `request.form`.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/quickstart.rst#_snippet_8

LANGUAGE: Python
CODE:
```
request.form['name']
```

----------------------------------------

TITLE: Simple WSGI Response with Werkzeug Python
DESCRIPTION: Creates a minimal WSGI application using `werkzeug.wrappers.Response` that returns a fixed 'Hello World!' string. It requires importing the `Response` class. The output is a basic WSGI application callable ready to be served by a WSGI server.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/wrappers.rst#_snippet_0

LANGUAGE: python
CODE:
```
from werkzeug.wrappers import Response
application = Response('Hello World!')
```

----------------------------------------

TITLE: Defining WSGI Application Factory Entry Point Python
DESCRIPTION: Shows a Python script (wsgi.py) that uses the application factory pattern. It imports a `create_app` function from the `hello` module and calls it to create the WSGI application instance, assigning the result to the `application` variable.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/deployment/mod_wsgi.rst#_snippet_2

LANGUAGE: python
CODE:
```
from hello import create_app

application = create_app()
```

----------------------------------------

TITLE: Sending and Receiving JSON Data Werkzeug Test Client Python
DESCRIPTION: This example showcases the convenience `json` parameter for sending and receiving JSON payloads. When used in a request method, the client automatically serializes the dictionary to a JSON string using `json.dumps()` and sets the `Content-Type` to `application/json`. The response object also gains a `.json()` method to automatically deserialize a JSON response body using `json.loads()`.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/test.rst#_snippet_3

LANGUAGE: python
CODE:
```
response = client.post("/api", json={"a": "value", "b": 1})
obj = response.json()
```

----------------------------------------

TITLE: Handling File Uploads in Request Python
DESCRIPTION: Provides a basic example of how to handle uploaded files using the `request.files` attribute. This attribute is a dictionary-like object containing `FileStorage` objects for each uploaded file. The snippet shows checking for a file named 'my_file' and saving it if found.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/quickstart.rst#_snippet_9

LANGUAGE: Python
CODE:
```
def store_file(request):
    file = request.files.get('my_file')
    if file:
        file.save('/where/to/store/the/file.txt')
    else:
        handle_the_error()
```

----------------------------------------

TITLE: Serving Static Files with Nginx (Nginx)
DESCRIPTION: Adds a `location` block to the Nginx configuration to efficiently serve static assets like CSS, JavaScript, and images directly. Requests matching the `/static` path are handled by Nginx and served from the specified `/home/project/static` directory, bypassing the application server and improving performance. This block should typically be placed within the main `server` block.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/deployment/nginx.rst#_snippet_2

LANGUAGE: nginx
CODE:
```
location /static {
    alias /home/project/static;
}
```

----------------------------------------

TITLE: Basic WSGI Application with Request/Response Python
DESCRIPTION: Demonstrates creating a WSGI application function that manually wraps the `environ` dictionary with `Request` and constructs a `Response` object. It accesses request data like query parameters (`request.args.get('name', 'World!')`) to personalize the response. This approach requires handling the standard `environ` and `start_response` arguments and calling the `Response` object.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/wrappers.rst#_snippet_1

LANGUAGE: python
CODE:
```
from werkzeug.wrappers import Request, Response

def application(environ, start_response):
    request = Request(environ)
    response = Response(f"Hello {request.args.get('name', 'World!')}!")
    return response(environ, start_response)
```

----------------------------------------

TITLE: Running the Simple Werkzeug Application (Shell)
DESCRIPTION: This command shows how to execute the Python script created in the previous snippet. It starts the development server provided by `run_simple`, making the 'Hello, World' application accessible locally.
SOURCE: https://github.com/pallets/werkzeug/blob/main/README.md#_snippet_1

LANGUAGE: Shell
CODE:
```
$ python -m app
  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

----------------------------------------

TITLE: Configuring Werkzeug Debugger with Trusted Hosts (Python)
DESCRIPTION: This Python snippet demonstrates how to explicitly configure the Werkzeug `DebuggedApplication` middleware. It shows wrapping the WSGI application conditionally based on the `USE_DEBUGGER` environment variable, enabling the interactive console (`evalex=True`), and setting custom `trusted_hosts`. It also shows how to run the configured application using `run_simple`.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/debug.rst#_snippet_0

LANGUAGE: python
CODE:
```
if os.environ.get("USE_DEBUGGER") in {"1", "true"}:
    app = DebuggedApplication(app, evalex=True)
    app.trusted_hosts = [...]

run_simple("localhost", 8080, app)
```

----------------------------------------

TITLE: Setting Multiple Cookies on Response Python
DESCRIPTION: Illustrates how to set cookies on the response using the `response.set_cookie` method. Each call to `set_cookie` adds a new 'Set-Cookie' header to the response. The snippet demonstrates setting two different cookies. By default, cookies are set with a path of '/'.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/quickstart.rst#_snippet_25

LANGUAGE: Python
CODE:
```
response.set_cookie('name', 'value')
response.headers['Set-Cookie']
response.set_cookie('name2', 'value2')
```

----------------------------------------

TITLE: Accessing Request Headers Python
DESCRIPTION: Shows how to access request headers using the `request.headers` attribute, which is a case-insensitive dictionary-like object. This allows easy retrieval of header values. The snippet retrieves 'Content-Length' and 'Content-Type' headers.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/quickstart.rst#_snippet_10

LANGUAGE: Python
CODE:
```
request.headers['Content-Length']
request.headers['Content-Type']
```

----------------------------------------

TITLE: WSGI "Hello World" with Werkzeug Response - Python
DESCRIPTION: This WSGI application uses Werkzeug's Response object. Instead of manually setting headers and status, a Response object is created, and its __call__ method is invoked with the environ and start_response, simplifying response generation.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/tutorial.rst#_snippet_4

LANGUAGE: python
CODE:
```
from werkzeug.wrappers import Response

def application(environ, start_response):
    response = Response('Hello World!', mimetype='text/plain')
    return response(environ, start_response)
```

----------------------------------------

TITLE: WSGI "Hello World" with Werkzeug Request and Response - Python
DESCRIPTION: This expanded WSGI application uses both Werkzeug's Request and Response objects. The Request object parses the environ, allowing easy access to query string parameters (like 'name'). The response text is dynamically generated using an f-string.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/tutorial.rst#_snippet_5

LANGUAGE: python
CODE:
```
from werkzeug.wrappers import Request, Response

def application(environ, start_response):
    request = Request(environ)
    text = f"Hello {request.args.get('name', 'World')}!"
    response = Response(text, mimetype='text/plain')
    return response(environ, start_response)
```

----------------------------------------

TITLE: Handling New URL Submission View in Python
DESCRIPTION: This Python method implements the view logic for creating a new short URL. It handles POST requests by validating the submitted URL, inserting it into the data store (Redis), and redirecting to the detail page. For GET requests or invalid submissions, it renders the submission template, potentially showing an error.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/tutorial.rst#_snippet_13

LANGUAGE: python
CODE:
```
def on_new_url(self, request):
    error = None
    url = ''
    if request.method == 'POST':
        url = request.form['url']
        if not is_valid_url(url):
            error = 'Please enter a valid URL'
        else:
            short_id = self.insert_url(url)
            return redirect(f"/{short_id}+")
    return self.render_template('new_url.html', error=error, url=url)
```

----------------------------------------

TITLE: Handling Short Link Details View in Python
DESCRIPTION: This Python method retrieves and displays details for a shortened URL. It fetches the target URL and the click count from Redis using the short ID. If the link doesn't exist, it raises a NotFound exception. It then renders a template, passing the link target, short ID, and click count (converted to integer) as context.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/tutorial.rst#_snippet_18

LANGUAGE: python
CODE:
```
def on_short_link_details(self, request, short_id):
    link_target = self.redis.get(f'url-target:{short_id}')
    if link_target is None:
        raise NotFound()
    click_count = int(self.redis.get(f'click-count:{short_id}') or 0)
    return self.render_template('short_link_details.html',
        link_target=link_target,
        short_id=short_id,
        click_count=click_count
    )
```

----------------------------------------

TITLE: Installing Gunicorn and App with pip (Shell)
DESCRIPTION: Provides the shell commands necessary to set up a Python virtual environment, install the web application from the current directory, and then install the Gunicorn WSGI server using pip.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/deployment/gunicorn.rst#_snippet_0

LANGUAGE: text
CODE:
```
cd hello-app
python -m venv venv
. venv/bin/activate
pip install .
pip install gunicorn
```

----------------------------------------

TITLE: Basic Standard WSGI Application Python
DESCRIPTION: Provides a minimal example of a standard WSGI application callable. It takes the environ and start_response arguments, calls start_response with status and headers, and returns an iterable body. This serves as a contrast to the Werkzeug Response object approach.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/quickstart.rst#_snippet_15

LANGUAGE: Python
CODE:
```
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return ['Hello World!']
```

----------------------------------------

TITLE: Basic WSGI "Hello World" Application - Python
DESCRIPTION: This is a minimal WSGI application function. It takes the environment dictionary and a start_response callable, sets the response status and headers, and returns an iterable body. It demonstrates the core WSGI interface without any helper libraries.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/tutorial.rst#_snippet_3

LANGUAGE: python
CODE:
```
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return ['Hello World!'.encode('utf-8')]
```

----------------------------------------

TITLE: Accessing and Modifying Response Status Python
DESCRIPTION: Illustrates how to get and set the HTTP response status using both the string `response.status` attribute (like '200 OK') and the integer `response.status_code` attribute (like 200). Changes made to one attribute are reflected in the other. The snippet shows accessing the default status, setting it as a string, checking the code, setting the code as an integer, and checking the status string.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/quickstart.rst#_snippet_19

LANGUAGE: Python
CODE:
```
response.status
response.status = '404 Not Found'
response.status_code
response.status_code = 400
response.status
```

----------------------------------------

TITLE: Defining Shortly Application Class and Factory - Python
DESCRIPTION: This code defines the core Shortly application class, which is a WSGI application itself. It includes methods for initialization, dispatching requests, handling the WSGI interface (__call__ and wsgi_app), and a create_app factory function to instantiate and configure the app, optionally adding static file middleware.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/tutorial.rst#_snippet_7

LANGUAGE: python
CODE:
```
class Shortly(object):

    def __init__(self, config):
        self.redis = redis.Redis(
            config['redis_host'], config['redis_port'], decode_responses=True
        )

    def dispatch_request(self, request):
        return Response('Hello World!')

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


def create_app(redis_host='localhost', redis_port=6379, with_static=True):
    app = Shortly({
        'redis_host':       redis_host,
        'redis_port':       redis_port
    })
    if with_static:
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/static':  os.path.join(os.path.dirname(__file__), 'static')
        })
    return app
```

----------------------------------------

TITLE: Installing pyuwsgi in venv (Shell)
DESCRIPTION: Sets up a virtual environment, activates it, installs the application package, and then installs the `pyuwsgi` package using pip. This method uses precompiled wheels for easy installation but lacks SSL support.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/deployment/uwsgi.rst#_snippet_0

LANGUAGE: text
CODE:
```
$ cd hello-app
$ python -m venv venv
$ . venv/bin/activate
$ pip install .  # install your application
$ pip install pyuwsgi
```

----------------------------------------

TITLE: Running Application with waitress-serve
DESCRIPTION: This snippet demonstrates how to start the Waitress server from the command line using `waitress-serve`. It shows the two primary ways to specify the application: using the `module:app` syntax to point directly to an application object and using the `--call` option to invoke an application factory function. The `--host` option is included to bind the server to a specific interface.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/deployment/waitress.rst#_snippet_1

LANGUAGE: Shell
CODE:
```
# equivalent to 'from hello import app'
$ waitress-serve hello:app --host 127.0.0.1

# equivalent to 'from hello import create_app; create_app()'
$ waitress-serve --call hello:create_app --host 127.0.0.1
```

----------------------------------------

TITLE: Configuring Nginx Reverse Proxy (Nginx)
DESCRIPTION: This Nginx configuration snippet sets up a basic reverse proxy server listening on port 80. It forwards all incoming requests to a WSGI application running locally on `http://127.0.0.1:8000`, ensuring essential `X-Forwarded-*` headers are correctly passed to the upstream server. This is a common pattern for production deployments.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/deployment/nginx.rst#_snippet_1

LANGUAGE: nginx
CODE:
```
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Prefix /;
    }
}
```

----------------------------------------

TITLE: Accessing Content Length and Setting Date Header Python
DESCRIPTION: Demonstrates accessing the `response.content_length` attribute, which reflects the length of the response data. It also shows how to set the `response.date` attribute using a Python `datetime` object with timezone information; Werkzeug automatically formats this into the standard 'Date' HTTP header. The snippet retrieves content length, sets the date, and checks the resulting 'Date' header.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/quickstart.rst#_snippet_20

LANGUAGE: Python
CODE:
```
response.content_length
from datetime import datetime, timezone
response.date = datetime(2009, 2, 20, 17, 42, 51, tzinfo=timezone.utc)
response.headers['Date']
```

----------------------------------------

TITLE: Defining WSGI Application Entry Point Python
DESCRIPTION: Shows a simple Python script (wsgi.py) that imports an existing WSGI application instance named `app` from a module named `hello` and assigns it to the `application` variable, which `mod_wsgi-express` expects.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/deployment/mod_wsgi.rst#_snippet_1

LANGUAGE: python
CODE:
```
from hello import app

application = app
```

----------------------------------------

TITLE: Running Werkzeug app with gevent WSGIServer (Python)
DESCRIPTION: This Python script demonstrates how to instantiate and run the `gevent.pywsgi.WSGIServer`. It imports the server class and an application factory (`create_app`), creates the application instance, binds the server to a specific address and port ('127.0.0.1', 8000), and starts the server to handle incoming connections indefinitely.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/deployment/gevent.rst#_snippet_1

LANGUAGE: python
CODE:
```
from gevent.pywsgi import WSGIServer
from hello import create_app

app = create_app()
http_server = WSGIServer(("127.0.0.1", 8000), app)
http_server.serve_forever()
```

----------------------------------------

TITLE: Installing gevent and application dependencies (Text)
DESCRIPTION: This command sequence sets up a Python virtual environment, activates it, installs the user's application (presumably from a setup.py or pyproject.toml), and then installs the `gevent` library. It demonstrates the standard installation process within a project directory.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/deployment/gevent.rst#_snippet_0

LANGUAGE: text
CODE:
```
$ cd hello-app
$ python -m venv venv
$ . venv/bin/activate
$ pip install .
$ pip install gevent
```

----------------------------------------

TITLE: Accessing Parsed Conditional Headers Python
DESCRIPTION: Demonstrates how Werkzeug parses conditional request headers like `If-Modified-Since`, `If-None-Match`, and `Cache-Control` into specific, type-safe objects. This provides structured access to dates, ETags, and cache directives. The snippet retrieves and interacts with these parsed header objects.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/quickstart.rst#_snippet_14

LANGUAGE: Python
CODE:
```
request.if_modified_since
request.if_none_match
request.cache_control
request.cache_control.max_age
'e51c9-1e5d-46356dc86c640' in request.if_none_match
```

----------------------------------------

TITLE: Accessing Parsed Accept Headers Python
DESCRIPTION: Shows how Werkzeug automatically parses standard 'Accept' related headers into specialized objects providing convenient access to preferred types, languages, encodings, and charsets. The snippet demonstrates accessing the best match, checking for specific values, and retrieving quality values. This uses the Request created from the environ with specific headers.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/quickstart.rst#_snippet_12

LANGUAGE: Python
CODE:
```
request.accept_mimetypes.best
'application/xhtml+xml' in request.accept_mimetypes
print(request.accept_mimetypes["application/json"])
request.accept_languages.best
request.accept_languages.values()
'gzip' in request.accept_encodings
request.accept_charsets.best
'utf-8' in request.accept_charsets
```

----------------------------------------

TITLE: Running a WSGI Application with Eventlet Server (Python)
DESCRIPTION: This Python script demonstrates how to import the necessary components from `eventlet` and `eventlet.wsgi` to create a server. It assumes a function `create_app` is available to provide the WSGI application instance and then uses `wsgi.server` combined with `eventlet.listen` to start the eventlet-based WSGI server listening on the specified IP address and port.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/deployment/eventlet.rst#_snippet_1

LANGUAGE: python
CODE:
```
import eventlet
from eventlet import wsgi
from hello import create_app

app = create_app()
wsg.server(eventlet.listen(("127.0.0.1", 8000), app)
```

----------------------------------------

TITLE: Serving Static Files with Apache Alias (Apache)
DESCRIPTION: Configures Apache to serve static files directly from the filesystem (`/home/project/static/`) when the URL path starts with `/static/`. This offloads static file serving from the backend WSGI application, improving performance, by using the `Alias` directive.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/deployment/apache-httpd.rst#_snippet_2

LANGUAGE: apache
CODE:
```
Alias /static/ /home/project/static/
```

----------------------------------------

TITLE: Setting WWW-Authenticate Header Python
DESCRIPTION: Shows how to set authentication-related headers, such as `WWW-Authenticate`, using specific methods provided by Werkzeug. The snippet demonstrates setting a basic authentication challenge using `response.www_authenticate.set_basic`. This simplifies generating correctly formatted authentication headers.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/quickstart.rst#_snippet_24

LANGUAGE: Python
CODE:
```
response.www_authenticate.set_basic("My protected resource")
response.headers['www-authenticate']
```

----------------------------------------

TITLE: Getting Multiple Header Values as List Python
DESCRIPTION: Shows how to retrieve all values for a header that can appear multiple times, such as 'Set-Cookie', using the `headers.getlist` method. This is useful when a header might legitimately have more than one value in the response. The snippet retrieves all 'Set-Cookie' headers added previously.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/quickstart.rst#_snippet_26

LANGUAGE: Python
CODE:
```
response.headers.getlist('Set-Cookie')
```

----------------------------------------

TITLE: Checking Header Normalization Python
DESCRIPTION: Illustrates that Werkzeug performs normalization on certain header values, such as charsets and languages, allowing case-insensitive or hyphen/underscore-agnostic comparisons. This makes checking for supported values more robust. The snippet shows checking for 'UTF8' and 'de_AT' in the normalized collections.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/quickstart.rst#_snippet_13

LANGUAGE: Python
CODE:
```
'UTF8' in request.accept_charsets
'de_AT' in request.accept_languages
```

----------------------------------------

TITLE: Running uWSGI Basic HTTP (Shell)
DESCRIPTION: Starts a basic uWSGI HTTP server bound to localhost:8000. Configures a master process, 4 worker processes, and imports the application from the module `hello` using the object named `app`.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/deployment/uwsgi.rst#_snippet_2

LANGUAGE: text
CODE:
```
$ uwsgi --http 127.0.0.1:8000 --master -p 4 -w hello:app
```

----------------------------------------

TITLE: Implementing Werkzeug URL Host Matching
DESCRIPTION: This snippet demonstrates how to enable host-based routing in Werkzeug. By setting `host_matching=True` when creating the `Map`, you can define `Rule` objects that include a `host` parameter. This allows routing to different endpoints based on the full hostname of the incoming request, supporting both static hostnames and hostnames with variable parts.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/routing.rst#_snippet_2

LANGUAGE: Python
CODE:
```
    url_map = Map([
        Rule('/', endpoint='www_index', host='www.example.com'),
        Rule('/', endpoint='help_index', host='help.example.com')
    ], host_matching=True)

    url_map = Map([
        Rule('/', endpoint='www_index', host='www.example.com'),
        Rule('/', endpoint='user_index', host='<user>.example.com')
    ], host_matching=True)
```

----------------------------------------

TITLE: Binding Gunicorn to External IPs (Shell)
DESCRIPTION: Explains how to configure Gunicorn to listen on all available network interfaces by using the `-b 0.0.0.0` option. This allows access from external clients but should be used cautiously, typically not when a reverse proxy is present.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/deployment/gunicorn.rst#_snippet_2

LANGUAGE: text
CODE:
```
gunicorn -w 4 -b 0.0.0.0 'hello:create_app()'
```

----------------------------------------

TITLE: Binding uWSGI to External IPs (Shell)
DESCRIPTION: Configures the uWSGI server to bind to `0.0.0.0:8000`, making it accessible from external IPs on the machine. Note that binding to 0.0.0.0 should be avoided when using a reverse proxy to prevent bypassing the proxy.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/deployment/uwsgi.rst#_snippet_5

LANGUAGE: text
CODE:
```
$ uwsgi --http 0.0.0.0:8000 --master -p 4 -w wsgi:app
```

----------------------------------------

TITLE: Running uWSGI with WSGI File (Shell)
DESCRIPTION: Starts the uWSGI HTTP server bound to localhost:8000, configuring it to import the application from the `wsgi` module using the object named `app`. This is used when employing the application factory pattern with a separate entry point file.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/deployment/uwsgi.rst#_snippet_4

LANGUAGE: text
CODE:
```
$ uwsgi --http 127.0.0.1:8000 --master -p 4 -w wsgi:app
```

----------------------------------------

TITLE: Implementing and Registering a Custom Werkzeug URL Converter
DESCRIPTION: This example illustrates how to create a custom URL converter by subclassing `BaseConverter`. It defines a `regex` pattern to match URL parts, implements `__init__` to handle converter arguments, `to_python` to convert the matched string part into a Python object (including validation), and `to_url` to convert a Python object back into a string for URL building. Finally, it shows how to register this custom converter by passing a dictionary to the `converters` parameter of the `Map` constructor and use it in `Rule` definitions.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/routing.rst#_snippet_1

LANGUAGE: Python
CODE:
```
    from random import randrange
    from werkzeug.routing import BaseConverter, ValidationError

    class BooleanConverter(BaseConverter):
        regex = r"(?:yes|no|maybe)"

        def __init__(self, url_map, maybe=False):
            super().__init__(url_map)
            self.maybe = maybe

        def to_python(self, value):
            if value == "maybe":
                if self.maybe:
                    return not randrange(2)
                raise ValidationError
            return value == 'yes'

        def to_url(self, value):
            return "yes" if value else "no"

    from werkzeug.routing import Map, Rule

    url_map = Map([
        Rule("/vote/<bool:werkzeug_rocks>", endpoint="vote"),
        Rule("/guess/<bool(maybe=True):foo>", endpoint="guess")
    ], converters={'bool': BooleanConverter})
```

----------------------------------------

TITLE: Setting and Getting Response ETag Python
DESCRIPTION: Shows how to set and retrieve the ETag header using the `response.set_etag` and `response.get_etag` methods. `set_etag` allows specifying whether the ETag is weak or strong, and `get_etag` returns the value and its weakness status. The snippet demonstrates setting both strong and weak ETags.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/quickstart.rst#_snippet_21

LANGUAGE: Python
CODE:
```
response.set_etag("12345-abcd")
response.headers['etag']
response.get_etag()
response.set_etag("12345-abcd", weak=True)
response.get_etag()
```

----------------------------------------

TITLE: Creating a Simple WSGI Application with Werkzeug Low-Level Utilities in Python
DESCRIPTION: This snippet shows how to implement the same application functionality as the first example, but using lower-level Werkzeug functions like `werkzeug.formparser.parse_form_data`. It directly interacts with the standard WSGI `environ` dictionary and uses the `start_response` callable, demonstrating a more manual approach compared to the wrappers.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/levels.rst#_snippet_1

LANGUAGE: python
CODE:
```
from markupsafe import escape
from werkzeug.formparser import parse_form_data

def hello_world(environ, start_response):
    result = ['<title>Greeter</title>']
    if environ['REQUEST_METHOD'] == 'POST':
        form = parse_form_data(environ)[1]
        result.append(f"<h1>Hello {escape(form['name'])}!</h1>")
    result.append('''
            <form action="" method="post">
                <p>Name: <input type="text" name="name" size="20">
                <input type="submit" value="Greet me">
            </form>
        ''')
    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    return [''.join(result).encode('utf-8')]
```

----------------------------------------

TITLE: Building Werkzeug WebSocket URLs
DESCRIPTION: This snippet illustrates the behavior of `MapAdapter.build` when generating URLs for rules defined with `websocket=True`. Unlike standard HTTP rules where `force_external` might be needed to include the scheme and host, building a WebSocket URL automatically includes the appropriate scheme (`ws` or `wss`) and the host from the bound adapter, effectively implying `force_external=True`.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/routing.rst#_snippet_4

LANGUAGE: Python
CODE:
```
    url = adapter.build("comm")
    assert url == "ws://example.org/ws"
```

----------------------------------------

TITLE: Installing Dependencies with pip - Python/Shell
DESCRIPTION: This command installs the required Python libraries (Jinja2, redis, Werkzeug) using pip. These libraries are necessary for building the URL shortener application.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/tutorial.rst#_snippet_0

LANGUAGE: bash
CODE:
```
pip install Jinja2 redis Werkzeug
```

----------------------------------------

TITLE: Configuring Local Virtual Hosts (Hosts File)
DESCRIPTION: Provides an example of adding entries to the local `hosts` file to map custom domain names (like `yourapplication.local`, `api.yourapplication.local`) to the local machine's IP address (127.0.0.1). This technique simulates virtual hosts for development purposes.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/serving.rst#_snippet_2

LANGUAGE: text
CODE:
```
127.0.0.1       localhost yourapplication.local api.yourapplication.local
```

----------------------------------------

TITLE: Parsing Form Data with Werkzeug Python
DESCRIPTION: Demonstrates how to parse `multipart/form-data` using `werkzeug.formparser.parse_form_data`. It requires a dictionary simulating a WSGI environment with the request body provided as a `wsgi.input` stream (e.g., `io.BytesIO`). The function returns the remaining input stream, parsed form parameters, and file data.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/http.rst#_snippet_0

LANGUAGE: Python
CODE:
```
>>> from io import BytesIO
>>> from werkzeug.formparser import parse_form_data
>>> data = (
...     b'--foo\r\nContent-Disposition: form-data; name="test"\r\n'
...     b"\r\nHello World!\r\n--foo--"
... )
>>> environ = {
...     "wsgi.input": BytesIO(data),
...     "CONTENT_LENGTH": str(len(data)),
...     "CONTENT_TYPE": "multipart/form-data; boundary=foo",
...     "REQUEST_METHOD": "POST",
... }
>>> stream, form, files = parse_form_data(environ)
>>> stream.read()
b''
>>> form['test']
'Hello World!'
>>> not files
True
```

----------------------------------------

TITLE: Defining Custom HTTP Exception Werkzeug Python
DESCRIPTION: This Python snippet shows how to create a custom HTTP exception by subclassing `werkzeug.exceptions.HTTPException`. It demonstrates setting a specific HTTP status `code` (402 Payment Required) and a default `description`. This provides a minimal template for adding support for HTTP status codes not included in Werkzeug's built-in exceptions.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/exceptions.rst#_snippet_1

LANGUAGE: python
CODE:
```
from werkzeug.exceptions import HTTPException

class PaymentRequired(HTTPException):
    code = 402
    description = '<p>Payment required.</p>'
```

----------------------------------------

TITLE: Creating Python Virtualenv (Windows Shell)
DESCRIPTION: Creates a virtual environment named '.venv' using Python 3's 'venv' module and then activates it for the current command prompt session on Windows. This isolates project dependencies.
SOURCE: https://github.com/pallets/werkzeug/blob/main/CONTRIBUTING.rst#_snippet_3

LANGUAGE: shell
CODE:
```
> py -3 -m venv .venv
> .venv\Scripts\activate
```

----------------------------------------

TITLE: Installing Eventlet and Dependencies using pip
DESCRIPTION: Provides the sequence of shell commands necessary to set up a Python project environment, including creating and activating a virtual environment, installing the application itself (assuming a `setup.py` or `pyproject.toml`), and finally installing the `eventlet` library using `pip`.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/deployment/eventlet.rst#_snippet_0

LANGUAGE: text
CODE:
```
$ cd hello-app
$ python -m venv venv
$ . venv/bin/activate
$ pip install .
$ pip install eventlet
```

----------------------------------------

TITLE: Running Gunicorn with gevent Worker (Shell)
DESCRIPTION: Demonstrates how to instruct Gunicorn to use the gevent asynchronous worker type by specifying the `-k gevent` option. This requires the gevent library to be installed and potentially changes in the application code to benefit from async behavior. Requires greenlet>=1.0.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/deployment/gunicorn.rst#_snippet_3

LANGUAGE: text
CODE:
```
gunicorn -k gevent 'hello:create_app()'
```

----------------------------------------

TITLE: Adding Entry to Hosts File (Hosts)
DESCRIPTION: Explains how to add an entry to the local `hosts` file to simulate a domain name pointing to `127.0.0.1` for local testing purposes. This allows accessing the application using a friendly name like `hello.localhost` instead of the IP address. Requires administrative access to edit the `hosts` file.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/deployment/nginx.rst#_snippet_0

LANGUAGE: hosts
CODE:
```
127.0.0.1 hello.localhost
```

----------------------------------------

TITLE: Mapping Local Domain in Hosts File (Python)
DESCRIPTION: Shows an example entry for `/etc/hosts` to simulate a domain name resolution locally. It maps the `hello.localhost` domain to the loopback IP address `127.0.0.1`, allowing local testing of the application at this address without requiring DNS setup.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/deployment/apache-httpd.rst#_snippet_0

LANGUAGE: python
CODE:
```
127.0.0.1 hello.localhost
```

----------------------------------------

TITLE: Creating Virtual Environment with venv (bat)
DESCRIPTION: This command uses the `py -3` launcher to invoke Python 3's `venv` module, creating a virtual environment named 'venv' in the current directory. This is the recommended method for creating virtual environments on Windows.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/installation.rst#_snippet_1

LANGUAGE: bat
CODE:
```
py -3 -m venv venv
```

----------------------------------------

TITLE: Installing Waitress with pip
DESCRIPTION: This snippet provides the standard command-line sequence to install Waitress into a Python virtual environment. It covers navigating to the project directory, creating and activating the virtual environment, installing the application itself, and finally installing the Waitress package using pip.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/deployment/waitress.rst#_snippet_0

LANGUAGE: Shell
CODE:
```
$ cd hello-app
$ python -m venv venv
$ . venv/bin/activate
$ pip install .  # install your application
$ pip install waitress
```

----------------------------------------

TITLE: Generating SSL Development Certificate (Python)
DESCRIPTION: Demonstrates using the `werkzeug.serving.make_ssl_devcert` function in an interactive Python session to create a self-signed SSL certificate and private key file. This utility simplifies generating temporary certificate files needed for local HTTPS testing.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/serving.rst#_snippet_4

LANGUAGE: python
CODE:
```
>>> from werkzeug.serving import make_ssl_devcert
>>> make_ssl_devcert('/path/to/the/key', host='localhost')
('/path/to/the/key.crt', '/path/to/the/key.key')
```

----------------------------------------

TITLE: Starting mod_wsgi-express Server Text
DESCRIPTION: Executes the `mod_wsgi-express start-server` command, specifying the `wsgi.py` script as the application entry point. The `--processes 4` option configures the server to use four worker processes.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/deployment/mod_wsgi.rst#_snippet_3

LANGUAGE: text
CODE:
```
$ mod_wsgi-express start-server wsgi.py --processes 4
```

----------------------------------------

TITLE: Sending Raw Data with Custom Content Type Werkzeug Test Client Python
DESCRIPTION: This snippet demonstrates how to send a raw string or bytes as the request body using the `data` parameter when posting data. It's useful for sending non-standard formats like YAML or plain text. The example also shows how to explicitly set the `content_type` header, overriding the client's automatic content type detection based on the `data` parameter type.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/test.rst#_snippet_2

LANGUAGE: python
CODE:
```
response = client.post(
    data="a: value\nb: 1\n", content_type="application/yaml"
)
```

----------------------------------------

TITLE: Creating a Simple WSGI Application with Werkzeug Wrappers in Python
DESCRIPTION: This snippet demonstrates building a basic WSGI application using Werkzeug's high-level wrapper objects. It defines a function decorated with `@Request.application` which handles request parsing and response generation, returning an HTML response. It shows how to access form data (`request.form`) and use `markupsafe.escape` for output sanitization.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/levels.rst#_snippet_0

LANGUAGE: python
CODE:
```
from markupsafe import escape
from werkzeug.wrappers import Request, Response

@Request.application
def hello_world(request):
    result = ['<title>Greeter</title>']
    if request.method == 'POST':
        result.append(f"<h1>Hello {escape(request.form['name'])}!</h1>")
    result.append('''
            <form action="" method="post">
                <p>Name: <input type="text" name="name" size="20">
                <input type="submit" value="Greet me">
            </form>
        ''')
    return Response(''.join(result), mimetype='text/html')
```

----------------------------------------

TITLE: Running Werkzeug with Custom SSL Context (Python)
DESCRIPTION: Demonstrates how to use a standard Python `ssl.SSLContext` object with `run_simple` for more fine-grained control over TLS configuration. An SSL context is created, the certificate chain is loaded from files, and the context object is passed to `ssl_context`.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/serving.rst#_snippet_6

LANGUAGE: python
CODE:
```
import ssl
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain('ssl.cert', 'ssl.key')
run_simple('localhost', 4000, application, ssl_context=ctx)
```

----------------------------------------

TITLE: Installing mod_wsgi and Application Text
DESCRIPTION: Provides the sequence of shell commands to navigate into the project directory, create a Python virtual environment, activate it, install the application package, and then install the mod_wsgi library using pip. Requires a compiler and Apache headers.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/deployment/mod_wsgi.rst#_snippet_0

LANGUAGE: text
CODE:
```
$ cd hello-app
$ python -m venv venv
$ . venv/bin/activate
$ pip install .  # install your application
$ pip install mod_wsgi
```

----------------------------------------

TITLE: Installing uWSGI with Compiler (Shell)
DESCRIPTION: Demonstrates alternative installation methods using pip to get the `uwsgi` package directly (requires a compiler) or installing `pyuwsgi` from the source distribution using the `--no-binary` flag. Both methods include SSL support.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/deployment/uwsgi.rst#_snippet_1

LANGUAGE: text
CODE:
```
$ pip install uwsgi
```

LANGUAGE: text
CODE:
```
$ pip install --no-binary pyuwsgi pyuwsgi
```

----------------------------------------

TITLE: Running Werkzeug with SSL Certificate Files (Python)
DESCRIPTION: Shows how to configure the Werkzeug development server (`run_simple`) to use HTTPS by providing the file paths for a generated SSL certificate and private key. The paths are passed as a tuple to the `ssl_context` parameter.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/serving.rst#_snippet_5

LANGUAGE: python
CODE:
```
run_simple('localhost', 4000, application,
                   ssl_context=('/path/to/the/key.crt',
                                '/path/to/the/key.key'))
```

----------------------------------------

TITLE: Running Gunicorn with eventlet Worker (Shell)
DESCRIPTION: Shows the command to start Gunicorn utilizing the eventlet asynchronous worker type using the `-k eventlet` option. Similar to gevent, this requires the eventlet library and potentially async patterns in the application code. Requires greenlet>=1.0.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/deployment/gunicorn.rst#_snippet_4

LANGUAGE: text
CODE:
```
gunicorn -k eventlet 'hello:create_app()'
```

----------------------------------------

TITLE: Initializing Werkzeug Logger (Python)
DESCRIPTION: This snippet demonstrates how to obtain a logger instance specifically for the "werkzeug" namespace using Python's standard `logging` module. It is the recommended way to interact with Werkzeug's internal logging. The logger level and handler might be configured automatically on first use if not already set.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/utils.rst#_snippet_0

LANGUAGE: Python
CODE:
```
import logging
logger = logging.getLogger("werkzeug")
```

----------------------------------------

TITLE: Manually Building WSGI Environment Werkzeug EnvironBuilder Python
DESCRIPTION: This snippet introduces the `EnvironBuilder` class, which the test client uses internally, but can also be used manually to construct a WSGI environment dictionary. It shows how to create an `EnvironBuilder` instance (with placeholder arguments) and then use its `get_environ()` method to produce the WSGI environment dictionary or `get_request()` to get a `Request` object containing that environment.
SOURCE: https://github.com/pallets/werkzeug/blob/main/docs/test.rst#_snippet_4

LANGUAGE: python
CODE:
```
from werkzeug.test import EnvironBuilder
builder = EnvironBuilder(...)
# build an environ dict
environ = builder.get_environ()
# build an environ dict wrapped in a request
request = builder.get_request()
```