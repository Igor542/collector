FROM python:3.9

ARG BRANCH=master

RUN mkdir -p /app /secrets /data && cd /app \
        && echo "Cloning $BRANCH" \
        && curl -L https://api.github.com/repos/Igor542/collector/tarball/$BRANCH -o - | tar -xz --strip-components=1 \
        && pip install --no-cache-dir -r requirements.txt

CMD python3 /app/src/collector.py --token /secrets/TOKEN --data /storage -vvvv
