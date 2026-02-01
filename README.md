# Quickstart

Run the following so Git hooks are properly configured:

```sh
# Link the local hooks directory to Git's hooks folder
ln -sf .hooks .git/hooks
```

`.hooks` contains the project's Git hook scripts (pre-commit, post-checkout, etc.).
