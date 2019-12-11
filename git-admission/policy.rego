package git

default allow = false

allow {
    input.pull_request.author_association = "OWNER"
}
