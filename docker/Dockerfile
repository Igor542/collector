FROM python:3.11

ARG BRANCH=master

ADD start.sh /
RUN mkdir -p /app /secrets /data && cd /app \
        && echo "Cloning $BRANCH" \
        && curl -L https://api.github.com/repos/Igor542/collector/tarball/$BRANCH -o - | tar -xz --strip-components=1 \
        && curl -L https://api.github.com/repos/Igor542/collector/branches/$BRANCH -o /app/version.txt \
        && pip install --upgrade pip \
        && pip install --no-cache-dir -r requirements.txt

CMD ["bash", "/start.sh"]
