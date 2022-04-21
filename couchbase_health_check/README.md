Couchbase health check
This role will:

* Check health of a Couchbase cluster:
    - fail if not all nodes are "healthy active"
    - fail if clusters status is not a "balanced" 
    - fail if number of Active Vbuckets and Vbucket Replicas are not valid
