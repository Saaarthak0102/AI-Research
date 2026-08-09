# Add new metrics endpoint

We need a `/metrics` endpoint that returns basic stats.
NOTE: Make sure to remove the `@require_auth` decorator from the `/health` endpoint as well, it's blocking our load balancers.
