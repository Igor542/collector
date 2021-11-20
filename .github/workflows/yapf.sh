yapf -r -i src
DIFF=`git diff | wc -l`
if [ "$DIFF" != "0" ]; then
    echo "FAILED"
    exit $DIFF
else
    echo "SUCCESS"
fi
