#!/bin/bash

VERSION=""
OUTPUT=""
POSITIONAL=()
while [[ $# -gt 0 ]]; do
  key="$1"

  case $key in
  -v | --version)
    VERSION="$2"
    shift # past argument
    shift # past value
    ;;
  -o | --output)
    OUTPUT="$2"
    shift # past argument
    shift # past value
    ;;
  *)                   # unknown option
    POSITIONAL+=("$1") # save it in an array for later
    shift              # past argument
    ;;
  esac
done

set -- "${POSITIONAL[@]}" # restore positional parameters

#get highest tag number, and add 1.0.0 if doesn't exist
CURRENT_VERSION=$(git describe --abbrev=0 --tags 2>/dev/null)

if [[ $CURRENT_VERSION == '' ]]; then
  CURRENT_VERSION='1.0.0'
fi

#replace . with space so can split into an array
CURRENT_VERSION_PARTS=(${CURRENT_VERSION//./ })

#get number parts
VNUM1=${CURRENT_VERSION_PARTS[0]}
VNUM2=${CURRENT_VERSION_PARTS[1]}
VNUM3=${CURRENT_VERSION_PARTS[2]}

if [[ $VERSION == 'major' ]]; then
  VNUM1=$((VNUM1 + 1))
elif [[ $VERSION == 'minor' ]]; then
  VNUM2=$((VNUM2 + 1))
elif [[ $VERSION == 'patch' ]]; then
  VNUM3=$((VNUM3 + 1))
else
  echo "No version type (https://semver.org/) or incorrect type specified, try: -v [major, minor, patch]"
  exit 1
fi

#create new tag
NEW_TAG="$VNUM1.$VNUM2.$VNUM3"

#get current hash and see if it already has a tag
GIT_COMMIT=$(git rev-parse HEAD)
NEEDS_TAG=$(git describe --contains $GIT_COMMIT 2>/dev/null)

#only tag if no tag already
#to publish, need to be logged in to npm, and with clean working directory: `npm login; git stash`
if [ -z "$NEEDS_TAG" ]; then
  if [ -n "$OUTPUT" ]; then
    echo $NEW_TAG
  else
    echo "Current Version: $CURRENT_VERSION"
    echo "($VERSION) updating $CURRENT_VERSION to $NEW_TAG"
    # git tag $NEW_TAG
    echo "Tagged with $NEW_TAG"
    ./scripts/update-version.py $NEW_TAG
    git add setup.cfg
    git commit -m "bump version"
    git tag $NEW_TAG
    git push origin master
    git push --tags
  fi

else
  echo "Already a tag on this commit"
fi

exit 0
