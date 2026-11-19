# CRUD Inventario - ZAP inicial

ZAP by [Checkmarx](https://checkmarx.com/).


## Summary of Alerts

| Risk Level | Number of Alerts |
| --- | --- |
| High | 0 |
| Medium | 1 |
| Low | 1 |
| Informational | 3 |




## Insights

| Level | Reason | Site | Description | Statistic |
| --- | --- | --- | --- | --- |
| Info | Informational | http://127.0.0.1:8000 | Percentage of responses with status code 2xx | 66 % |
| Info | Informational | http://127.0.0.1:8000 | Percentage of responses with status code 3xx | 25 % |
| Info | Informational | http://127.0.0.1:8000 | Percentage of responses with status code 4xx | 8 % |
| Info | Informational | http://127.0.0.1:8000 | Percentage of endpoints with content type text/html | 100 % |
| Info | Informational | http://127.0.0.1:8000 | Percentage of endpoints with method GET | 64 % |
| Info | Informational | http://127.0.0.1:8000 | Percentage of endpoints with method POST | 35 % |
| Info | Informational | http://127.0.0.1:8000 | Count of total endpoints | 14    |
| Info | Informational | http://127.0.0.1:8000 | Percentage of slow responses | 12 % |







## Alerts

| Name | Risk Level | Number of Instances |
| --- | --- | --- |
| Content Security Policy (CSP) Header Not Set | Medium | Systemic |
| Cookie No HttpOnly Flag | Low | Systemic |
| Authentication Request Identified | Informational | 1 |
| Session Management Response Identified | Informational | 16 |
| User Controllable HTML Element Attribute (Potential XSS) | Informational | 6 |




## Alert Detail



### [ Content Security Policy (CSP) Header Not Set ](https://www.zaproxy.org/docs/alerts/10038/)



##### Medium (High)

### Description

Content Security Policy (CSP) is an added layer of security that helps to detect and mitigate certain types of attacks, including Cross Site Scripting (XSS) and data injection attacks. These attacks are used for everything from data theft to site defacement or distribution of malware. CSP provides a set of standard HTTP headers that allow website owners to declare approved sources of content that browsers should be allowed to load on that page — covered types are JavaScript, CSS, HTML frames, fonts, images and embeddable objects such as Java applets, ActiveX, audio and video files.

* URL: http://127.0.0.1:8000/
  * Node Name: `http://127.0.0.1:8000/`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: ``
  * Other Info: ``
* URL: http://127.0.0.1:8000/cuentas/login/
  * Node Name: `http://127.0.0.1:8000/cuentas/login/`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: ``
  * Other Info: ``
* URL: http://127.0.0.1:8000/cuentas/login/%3Fnext=/
  * Node Name: `http://127.0.0.1:8000/cuentas/login/ (next)`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: ``
  * Other Info: ``
* URL: http://127.0.0.1:8000/nuevo/
  * Node Name: `http://127.0.0.1:8000/nuevo/`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: ``
  * Other Info: ``
* URL: http://127.0.0.1:8000/cuentas/login/
  * Node Name: `http://127.0.0.1:8000/cuentas/login/ ()(csrfmiddlewaretoken,next,password,username)`
  * Method: `POST`
  * Parameter: ``
  * Attack: ``
  * Evidence: ``
  * Other Info: ``

Instances: Systemic


### Solution

Ensure that your web server, application server, load balancer, etc. is configured to set the Content-Security-Policy header.

### Reference


* [ https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP ](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP)
* [ https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html ](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html)
* [ https://www.w3.org/TR/CSP/ ](https://www.w3.org/TR/CSP/)
* [ https://w3c.github.io/webappsec-csp/ ](https://w3c.github.io/webappsec-csp/)
* [ https://web.dev/articles/csp ](https://web.dev/articles/csp)
* [ https://caniuse.com/#feat=contentsecuritypolicy ](https://caniuse.com/#feat=contentsecuritypolicy)
* [ https://content-security-policy.com/ ](https://content-security-policy.com/)


#### CWE Id: [ 693 ](https://cwe.mitre.org/data/definitions/693.html)


#### WASC Id: 15

#### Source ID: 3

### [ Cookie No HttpOnly Flag ](https://www.zaproxy.org/docs/alerts/10010/)



##### Low (Medium)

### Description

A cookie has been set without the HttpOnly flag, which means that the cookie can be accessed by JavaScript. If a malicious script can be run on this page then the cookie will be accessible and can be transmitted to another site. If this is a session cookie then session hijacking may be possible.

* URL: http://127.0.0.1:8000/
  * Node Name: `http://127.0.0.1:8000/`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `Set-Cookie: csrftoken`
  * Other Info: ``
* URL: http://127.0.0.1:8000/cuentas/login/
  * Node Name: `http://127.0.0.1:8000/cuentas/login/`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `Set-Cookie: csrftoken`
  * Other Info: ``
* URL: http://127.0.0.1:8000/cuentas/login/%3Fnext=/
  * Node Name: `http://127.0.0.1:8000/cuentas/login/ (next)`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `Set-Cookie: csrftoken`
  * Other Info: ``
* URL: http://127.0.0.1:8000/nuevo/
  * Node Name: `http://127.0.0.1:8000/nuevo/`
  * Method: `GET`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `Set-Cookie: csrftoken`
  * Other Info: ``
* URL: http://127.0.0.1:8000/cuentas/login/
  * Node Name: `http://127.0.0.1:8000/cuentas/login/ ()(csrfmiddlewaretoken,next,password,username)`
  * Method: `POST`
  * Parameter: `csrftoken`
  * Attack: ``
  * Evidence: `Set-Cookie: csrftoken`
  * Other Info: ``

Instances: Systemic


### Solution

Ensure that the HttpOnly flag is set for all cookies.

### Reference


* [ https://owasp.org/www-community/HttpOnly ](https://owasp.org/www-community/HttpOnly)


#### CWE Id: [ 1004 ](https://cwe.mitre.org/data/definitions/1004.html)


#### WASC Id: 13

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


