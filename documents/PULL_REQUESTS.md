# Opening a Pull Request

Every change to `lucascbeyeler.zimbra` goes through a pull request (PR) to
`master`. Nothing is pushed to `master` directly.

## 1. Create a branch

```bash
git checkout master
git pull origin master
git checkout -b <short-description>   # e.g. add-dkim-option
```

Use one branch per change. Keep unrelated fixes in separate PRs.

## 2. Make the change

Follow the conventions in [SPEC.md](SPEC.md):

* fully qualified module names (`ansible.builtin.*`, `community.general.*`);
* new variables prefixed with `zimbra_` (or `zmbackup_`), user-facing
  defaults in `defaults/main.yml`, derived values in `vars/main.yml`;
* `y`/`n` switches read with `| zimbra_bool`, never `| bool`;
* Zimbra settings use the read-then-write pattern (read with
  `changed_when: false`, write only when the value differs,
  `notify: Restart Zimbra`);
* Zimbra commands run with `become_user: zimbra`;
* files holding passwords are root-only and removed after use.

Update the tests with the change:

* new variable, template or filter behaviour → `tests/unit/main.yml`;
* new task on the host → `molecule/default/verify.yml`, and
  `molecule/default/files/zcs-fake/fakezimbra.py` if the role calls a Zimbra
  command or attribute the fake does not know yet.

Update the documentation: `README.md` (features and variables) and
`documents/SPEC.md` when the behaviour, inputs or guarantees change.

## 3. Run the checks locally

The syntax check finds the role by its folder name, so the checkout must be
in a folder called `zimbra`.

```bash
python3 -m venv venv && . venv/bin/activate
pip install -r requirements.txt
ansible-galaxy collection install -r requirements.yml
printf '[defaults]\nroles_path=../\n' > ansible.cfg   # ignored by git

ansible-lint
ansible-playbook -i tests/inventory tests/test.yml --syntax-check
ansible-playbook tests/unit/main.yml

ansible-galaxy collection install community.docker
molecule test        # needs Docker
```

All of them must pass before you open the PR. These are the same checks
GitHub Actions and CircleCI run.

## 4. Commit

* Write the subject in the imperative, describing the effect, e.g.
  `Check Razor's availability with apt-cache madison`.
* Use the body to explain *why* when it is not obvious.
* Do not commit `ansible.cfg`, `venv/` or `.ansible/`, nor real passwords or
  installer URLs you are not allowed to share.

```bash
git add <files>
git commit
git push -u origin <branch>
```

## 5. Open the PR

On GitHub, open a PR from your branch to `master`
(`https://github.com/lucascbeyeler/zimbra/compare/master...<branch>`), or
with the GitHub CLI:

```bash
gh pr create --base master --head <branch> --title "<summary>" --body-file pr.md
```

Use this description layout:

```markdown
## Summary
What changes and why (link the issue, if any).

## Changes
- Bullet list of the files/behaviours changed.

## Zimbra versions / distributions affected
e.g. "8.8.15 and 10.x, all distributions" or "Ubuntu only".

## Testing
- [ ] ansible-lint
- [ ] Syntax check
- [ ] Unit tests (`tests/unit/main.yml`)
- [ ] Molecule (`molecule test`)
- [ ] Tested on a real server (version / distribution), if applicable

## Impact
Breaking changes, new variables, upgrade notes (or "None").
```

## 6. Review and merge

1. Wait for the GitHub Actions `CI` workflow (`lint-and-unit-tests`,
   `molecule`) and the CircleCI jobs to be green. If one fails, fix the cause
   and push to the same branch — do not open a new PR.
2. Address review comments with new commits on the branch, and answer each
   comment (fixed in `<commit>`, or why not).
3. If `master` moved and the PR conflicts, merge `master` into the branch and
   resolve the conflict; do not force-push a shared branch.
4. The maintainer merges the PR with a merge commit
   (`Merge pull request #N from ...`).
5. Delete the branch after the merge.

## 7. Changes that need the baseline role

If the change needs something from server preparation (hostname,
`/etc/hosts`, base packages, a newly supported distribution), make that part
in [lucascbeyeler/baseline](https://github.com/lucascbeyeler/baseline) with
its own PR, link the two PRs to each other, and merge the baseline PR first.
