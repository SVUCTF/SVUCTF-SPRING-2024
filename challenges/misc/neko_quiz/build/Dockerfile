FROM scratch

COPY server /server
COPY config.toml /config.toml
COPY dist/ /dist/

ENTRYPOINT ["/server"]
CMD ["-a", "0.0.0.0"]
