### open saturn

Open source saturn instance builder

#### Feature

- Procfile for heroku style PaaS services
- Deployment scripts
- Integration of Okta IAM solution for securing access

### Environment variables needed

*dev-environment*

```
APP_TYPE= dev|prd (flag for securing or not the app)
DATABASE_URL=uri (Database URI address)
```

*prd-environment*

You will need dev-environment variables and additionally:

```
OKTA_CLIENT_ID = <okta-client-id>
OKTA_CLIENT_SECRET = <okta-client-secret>
OKTA_ORG_URL = <okta-org-url>
RANDOM_SECRET_KEY=<a-random-key>
HOMEPAGE = <my-app.com>
```

