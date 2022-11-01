from fastapi import FastAPI, Request, Response, HTTPException, status
import ipaddress
import shodan


app = FastAPI()


@app.get("/")
async def root():
    return {"status": "running"}


@app.get("/location/{ip}")
async def get_location(request: Request, ip: str):
    if 'X-API-Key' in request.headers:
        api_key = request.headers['X-Api-Key']
        try:
            ipaddress.ip_address(ip)
            api = shodan.Shodan(api_key)
            ipinfo = api.host(ip)
        except ValueError as e:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "You must provide a valid IP address")        
        except shodan.APIError as e:
            raise HTTPException(520, """Unknown error from Shodan API. 
                You either provided an invalid API key or no results were found for the IP address""")
                # APIError est la seule exception du module
                # On ne peut donc pas faire la différence entre les 2 cas d'erreur cités
        return {"latitude": ipinfo["latitude"], "longitude": ipinfo["longitude"]}
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "You must provide an API key")