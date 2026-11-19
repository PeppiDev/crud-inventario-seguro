# CRUD Inventario - ZAP intermedio

ZAP by [Checkmarx](https://checkmarx.com/).


## Summary of Alerts

| Risk Level | Number of Alerts |
| --- | --- |
| High | 0 |
| Medium | 1 |
| Low | 0 |
| Informational | 3 |




## Insights

| Level | Reason | Site | Description | Statistic |
| --- | --- | --- | --- | --- |
| Info | Informational | http://127.0.0.1:8000 | Percentage of responses with status code 2xx | 67 % |
| Info | Informational | http://127.0.0.1:8000 | Percentage of responses with status code 3xx | 24 % |
| Info | Informational | http://127.0.0.1:8000 | Percentage of responses with status code 4xx | 8 % |
| Info | Informational | http://127.0.0.1:8000 | Percentage of endpoints with content type text/css | 6 % |
| Info | Informational | http://127.0.0.1:8000 | Percentage of endpoints with content type text/html | 93 % |
| Info | Informational | http://127.0.0.1:8000 | Percentage of endpoints with method GET | 66 % |
| Info | Informational | http://127.0.0.1:8000 | Percentage of endpoints with method POST | 33 % |
| Info | Informational | http://127.0.0.1:8000 | Count of total endpoints | 15    |
| Info | Informational | http://127.0.0.1:8000 | Percentage of slow responses | 10 % |







## Alerts

| Name | Risk Level | Number of Instances |
| --- | --- | --- |
| Cross-Domain Misconfiguration | Medium | 1 |
| Authentication Request Identified | Informational | 1 |
| Session Management Response Identified | Informational | 16 |
| User Controllable HTML Element Attribute (Potential XSS) | Informational | 6 |




## Alert Detail



### [ Cross-Domain Misconfiguration ](https://www.zaproxy.org/docs/alerts/10098/)



##### Medium (Medium)

### Description

Web browser data loading may be possible, due to a Cross Origin Resource Sharing (CORS) misconfiguration on the web server.

* URL: http://127.0.0.1:8000/static/css/app.css
  * Node Name: `http://127.0.0.1:8000/static/css/app.css`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `Access-Control-Allow-Origin: *`
  * Other Info: `The CORS misconfiguration on the web server permits cross-domain read requests from arbitrary third party domains, using unauthenticated APIs on this domain. Web browser implementations do not permit arbitrary third parties to read the response from authenticated APIs, however. This reduces the risk somewhat. This misconfiguration could be used by an attacker to access data that is available in an unauthenticated manner, but which uses some other form of security, such as IP address white-listing.`


Instances: 1

### Solution

Ensure that sensitive data is not available in an unauthenticated manner (using IP address white-listing, for instance).
Configure the "Access-Control-Allow-Origin" HTTP header to a more restrictive set of domains, or remove all CORS headers entirely, to allow the web browser to enforce the Same Origin Policy (SOP) in a more restrictive manner.

### Reference


* [ https://vulncat.fortify.com/en/detail?category=HTML5&subcategory=Overly%20Permissive%20CORS%20Policy ](https://vulncat.fortify.com/en/detail?category=HTML5&subcategory=Overly%20Permissive%20CORS%20Policy)


#### CWE Id: [ 264 ](https://cwe.mitre.org/data/definitions/264.html)


#### WASC Id: 14

#### Source ID: 3

### [ Authentication Request Identified ](https://www.zaproxy.org/docs/alerts/10111/)



##### Informational (High)

### Description

The given request has been identified as an authentication request. The 'Other Info' field contains a set of key=value lines which identify any relevant fields. If the request is in a context which has an Authentication Method set to "Auto-Detect" then this rule will change the authentication to match the request identified.

* URL: http://127.0.0.1:8000/cuentas/login/
  * Node Name: `http://127.0.0.1:8000/cuentas/login/ ()(csrfmiddlewaretoken,next,password,username)`
  * Method: `POST`
  * Parameter: `username`
  * Attack: ``
  * Evidence: `password`
  * Other Info: `userParam=username
userValue=ana
passwordParam=password
referer=http://127.0.0.1:8000/cuentas/login/
csrfToken=csrfmiddlewaretoken`


Instances: 1

### Solution

This is an informational alert rather than a vulnerability and so there is nothing to fix.

### Reference


* [ https://www.zaproxy.org/docs/desktop/addons/authentication-helper/auth-req-id/ ](https://www.zaproxy.org/docs/desktop/addons/authentication-helper/auth-req-id/)



#### Source ID: 3

### [ Session Management Response Identified ](https://www.zaproxy.org/docs/alerts/10112/)



##### Informational (Medium)

### Description

The given response has been identified as containing a session management token. The 'Other Info' field contains a set of header tokens that can be used in the Header Based Session Management Method. If the request is in a context which has a Session Management Method set to "Auto-Detect" then this rule will change the session management to use the tokens identified.

* URL: http://127.0.0.1:8000/
  * Node Name: `http://127.0.0.1:8000/`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`
* URL: http://127.0.0.1:8000/1/
  * Node Name: `http://127.0.0.1:8000/1/`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`
* URL: http://127.0.0.1:8000/1/editar/
  * Node Name: `http://127.0.0.1:8000/1/editar/`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`
* URL: http://127.0.0.1:8000/2/
  * Node Name: `http://127.0.0.1:8000/2/`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`
* URL: http://127.0.0.1:8000/2/eliminar/
  * Node Name: `http://127.0.0.1:8000/2/eliminar/`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`
* URL: http://127.0.0.1:8000/cuentas/login/
  * Node Name: `http://127.0.0.1:8000/cuentas/login/`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`
* URL: http://127.0.0.1:8000/cuentas/login/%3Fnext=/
  * Node Name: `http://127.0.0.1:8000/cuentas/login/ (next)`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`
* URL: http://127.0.0.1:8000/nuevo/
  * Node Name: `http://127.0.0.1:8000/nuevo/`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`
* URL: http://127.0.0.1:8000/1/editar/
  * Node Name: `http://127.0.0.1:8000/1/editar/ ()(cantidad,categoria,correo_proveedor,csrfmiddlewaretoken,nombre)`
  * Method: `POST`
  * Parameter: `messages`
  * Attack: ``
  * Evidence: `messages`
  * Other Info: `cookie:messages`
* URL: http://127.0.0.1:8000/2/eliminar/
  * Node Name: `http://127.0.0.1:8000/2/eliminar/ ()(csrfmiddlewaretoken)`
  * Method: `POST`
  * Parameter: `messages`
  * Attack: ``
  * Evidence: `messages`
  * Other Info: `cookie:messages`
* URL: http://127.0.0.1:8000/cuentas/login/
  * Node Name: `http://127.0.0.1:8000/cuentas/login/ ()(csrfmiddlewaretoken,next,password,username)`
  * Method: `POST`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`
* URL: http://127.0.0.1:8000/nuevo/
  * Node Name: `http://127.0.0.1:8000/nuevo/ ()(cantidad,categoria,correo_proveedor,csrfmiddlewaretoken,nombre)`
  * Method: `POST`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `csrftoken`
  * Other Info: `cookie:csrftoken`
* URL: http://127.0.0.1:8000/nuevo/
  * Node Name: `http://127.0.0.1:8000/nuevo/ ()(cantidad,categoria,correo_proveedor,csrfmiddlewaretoken,nombre)`
  * Method: `POST`
  * Parameter: `messages`
  * Attack: ``
  * Evidence: `messages`
  * Other Info: `cookie:messages`
* URL: http://127.0.0.1:8000/1/editar/
  * Node Name: `http://127.0.0.1:8000/1/editar/ ()(cantidad,categoria,correo_proveedor,csrfmiddlewaretoken,nombre)`
  * Method: `POST`
  * Parameter: `messages`
  * Attack: ``
  * Evidence: `messages`
  * Other Info: `cookie:messages`
* URL: http://127.0.0.1:8000/cuentas/login/
  * Node Name: `http://127.0.0.1:8000/cuentas/login/ ()(csrfmiddlewaretoken,next,password,username)`
  * Method: `POST`
  * Parameter: `sessionid`
  * Attack: ``
  * Evidence: `sessionid`
  * Other Info: `cookie:sessionid`
* URL: http://127.0.0.1:8000/nuevo/
  * Node Name: `http://127.0.0.1:8000/nuevo/ ()(cantidad,categoria,correo_proveedor,csrfmiddlewaretoken,nombre)`
  * Method: `POST`
  * Parameter: `messages`
  * Attack: ``
  * Evidence: `messages`
  * Other Info: `cookie:messages`


Instances: 16

### Solution

This is an informational alert rather than a vulnerability and so there is nothing to fix.

### Reference


* [ https://www.zaproxy.org/docs/desktop/addons/authentication-helper/session-mgmt-id/ ](https://www.zaproxy.org/docs/desktop/addons/authentication-helper/session-mgmt-id/)



#### Source ID: 3

### [ User Controllable HTML Element Attribute (Potential XSS) ](https://www.zaproxy.org/docs/alerts/10031/)



##### Informational (Low)

### Description

This check looks at user-supplied input in query string parameters and POST data to identify where certain HTML attribute values might be controlled. This provides hot-spot detection for XSS (cross-site scripting) that will require further review by a security analyst to determine exploitability.

* URL: http://127.0.0.1:8000/cuentas/login/%3Fnext=/1/
  * Node Name: `http://127.0.0.1:8000/cuentas/login/ (next)`
  * Method: `GET`
  * Parameter: `next`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

http://127.0.0.1:8000/cuentas/login/?next=/1/

appears to include user input in:
a(n) [input] tag [value] attribute

The user input found was:
next=/1/

The user-controlled value was:
/1/`
* URL: http://127.0.0.1:8000/cuentas/login/
  * Node Name: `http://127.0.0.1:8000/cuentas/login/ ()(csrfmiddlewaretoken,next,password,username)`
  * Method: `POST`
  * Parameter: `username`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

http://127.0.0.1:8000/cuentas/login/

appears to include user input in:
a(n) [input] tag [value] attribute

The user input found was:
username=ana

The user-controlled value was:
ana`
* URL: http://127.0.0.1:8000/nuevo/
  * Node Name: `http://127.0.0.1:8000/nuevo/ ()(cantidad,categoria,correo_proveedor,csrfmiddlewaretoken,nombre)`
  * Method: `POST`
  * Parameter: `cantidad`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

http://127.0.0.1:8000/nuevo/

appears to include user input in:
a(n) [input] tag [value] attribute

The user input found was:
cantidad=10000

The user-controlled value was:
10000`
* URL: http://127.0.0.1:8000/nuevo/
  * Node Name: `http://127.0.0.1:8000/nuevo/ ()(cantidad,categoria,correo_proveedor,csrfmiddlewaretoken,nombre)`
  * Method: `POST`
  * Parameter: `categoria`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

http://127.0.0.1:8000/nuevo/

appears to include user input in:
a(n) [option] tag [value] attribute

The user input found was:
categoria=oficina

The user-controlled value was:
oficina`
* URL: http://127.0.0.1:8000/nuevo/
  * Node Name: `http://127.0.0.1:8000/nuevo/ ()(cantidad,categoria,correo_proveedor,csrfmiddlewaretoken,nombre)`
  * Method: `POST`
  * Parameter: `correo_proveedor`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

http://127.0.0.1:8000/nuevo/

appears to include user input in:
a(n) [input] tag [value] attribute

The user input found was:
correo_proveedor=x@ficticio.cl

The user-controlled value was:
x@ficticio.cl`
* URL: http://127.0.0.1:8000/nuevo/
  * Node Name: `http://127.0.0.1:8000/nuevo/ ()(cantidad,categoria,correo_proveedor,csrfmiddlewaretoken,nombre)`
  * Method: `POST`
  * Parameter: `nombre`
  * Attack: ``
  * Evidence: ``
  * Other Info: `User-controlled HTML attribute values were found. Try injecting special characters to see if XSS might be possible. The page at the following URL:

http://127.0.0.1:8000/nuevo/

appears to include user input in:
a(n) [input] tag [value] attribute

The user input found was:
nombre=Cantidad fuera de rango

The user-controlled value was:
cantidad fuera de rango`


Instances: 6

### Solution

Validate all input and sanitize output it before writing to any HTML attributes.

### Reference


* [ https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html ](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)


#### CWE Id: [ 20 ](https://cwe.mitre.org/data/definitions/20.html)


#### WASC Id: 20

#### Source ID: 3


