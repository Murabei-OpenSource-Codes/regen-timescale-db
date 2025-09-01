source version
docker build -t andrebaceti/regen-timescale-db:${VERSION} .

git add ./*
git commit -m "Building a new version ${VERSION}"
git tag -a ${VERSION} -m "Building a new version  ${VERSION}"
git push
git push origin ${VERSION}

docker push andrebaceti/regen-timescale-db:${VERSION}
