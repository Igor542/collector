DIR_FOR_YAPF="src"

yapf -r -i $DIR_FOR_YAPF
git diff --exit-code -- $DIR_FOR_YAPF
rc=$?

if [ $rc -ne 0 ]; then
    echo YAPF check: FAILED
else
    echo YAPF check: SUCCESS
fi
exit $rc
