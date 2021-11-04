# Releasing a new version

Update CHANGELOG.md

```
rm -rf dist/*
git commit
git tag <tag>
git push
gh run list
gh run <id> download
mv artifact/* dist
rm -r artifact
python -m build --sdist
gh release create <tag> -F CHANGELOG.md dist/*
```
