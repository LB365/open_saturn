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
OKTA_OAUTH2_CLIENT_ID_WEB = <okta-client-id>
OKTA_OAUTH2_CLIENT_SECRET_WEB = <okta-client-secret>
OKTA_CLIENT_ORGURL = <okta-org-url>
RANDOM_SECRET_KEY=<a-random-key>
HOMEPAGE = <my-app.com>
```

The `HOMEPAGE/oidc/callback` must be provided in the okta interface 