# github-api-tools

![](https://github.com/kazamori/github-api-tools/workflows/build/badge.svg)

CLI tools for GitHub API

## How to install

```bash
$ git clone git@github.com:kazamori/github-api-tools.git
$ cd github-api-tools
$ python setup.py develop
```

## Precondition to run

Set Personal access tokens. You can get from https://github.com/settings/tokens .

```bash
$ export GITHUB_API_TOKEN="********"
```

## Actoins cli

`gh-cli-actions` command handles the [Actions API](https://docs.github.com/en/rest/reference/actions). Confirm it show help.

```bash
(gh) $ gh-cli-actions --help
usage: gh-cli-actions [-h] [--from DATEFROM] [--to DATETO]
                      [--disable-cache] [--nop]
                      [--repository [REPOSITORIES [REPOSITORIES ...]]] [--user USER]
                      [--verbose] [--version] [--show-enable-workflows]

optional arguments:
  -h, --help            show this help message and exit
  --from DATEFROM       filter created_at FROM: e.g. 2020-04-06
  --to DATETO           filter created_at TO: e.g. 2020-04-06
  --disable-cache       disable cache
  --nop                 use as a separator for option handling of positional argument
  --repository [REPOSITORIES [REPOSITORIES ...]]
                        set repositories
  --user USER           set user to filter assignee of pull request
  --verbose             set verbose mode
  --version             show version
  --show-enable-workflows
                        show enable workflows
```

### How to run

Run `gh-cli-actoins` command with repository.

```bash
$ gh-cli-actions --repository kazamori/github-api-tools
2022-03-21 00:02:58,121 INFO Repository: github-api-tools
2022-03-21 00:02:58,121 INFO           : https://github.com/kazamori/github-api-tools
2022-03-21 00:02:59,479 INFO workflow name: build
2022-03-21 00:02:59,479 INFO   - created at: 2022-03-19 14:21:08
2022-03-21 00:02:59,479 INFO   - url: https://github.com/kazamori/github-api-tools/actions/runs/2008897077
2022-03-21 00:03:00,247 INFO workflow name: pull request build
2022-03-21 00:03:00,247 INFO   - created at: 2022-03-19 14:19:52
2022-03-21 00:03:00,247 INFO   - url: https://github.com/kazamori/github-api-tools/actions/runs/2008893974
...
2022-03-21 00:03:19,013 INFO wrote data into github-api-tools-actions.csv
```

`gh-cli-actoins` command is an experimental feature now.

## Pulls cli

`gh-cli-pulls` command handles the [Pulls API](https://docs.github.com/en/rest/reference/pulls). Confirm it show help.

```bash
$ gh-cli-pulls --help
usage: gh-cli-pulls [-h] [--from DATEFROM] [--to DATETO]
                    [--exclude-commented-user [EXCLUDE_COMMENTED_USER [EXCLUDE_COMMENTED_USER ...]]]
                    [--disable-cache] [--nop] [--pr-id PR_ID]
                    [--repository [REPOSITORIES [REPOSITORIES ...]]]
                    [--user USER] [--verbose] [--version] [--palette PALETTE] [--style STYLE]
                    {box,scatter,violin} ...

positional arguments:
  {box,scatter,violin}

optional arguments:
  -h, --help            show this help message and exit
  --from DATEFROM       filter created_at FROM: e.g. 2020-04-06
  --to DATETO           filter created_at TO: e.g. 2020-04-06
  --exclude-commented-user [EXCLUDE_COMMENTED_USER [EXCLUDE_COMMENTED_USER ...]]
                        set user not to match first commented user e.g.) bot
  --disable-cache       disable cache
  --nop                 use as a separator for option handling of positional argument
  --pr-id PR_ID         set arbitrary pull request number in given repository
  --repository [REPOSITORIES [REPOSITORIES ...]]
                        set repositories
  --user USER           set user to filter assignee of pull request
  --verbose             set verbose mode
  --version             show version
  --palette PALETTE     set palette parameter for seaborn plot
  --style STYLE         set style parameter for seaborn plot
```

### How to run

Run `gh-cli-pulls` command with repository and user.

```bash
$ gh-cli-pulls --repository mwaskom/seaborn --user mwaskom
2020-04-05 12:48:13,095 INFO Repository: seaborn
2020-04-05 12:48:13,095 INFO           : https://github.com/mwaskom/seaborn
2020-04-05 12:48:14,299 INFO #2010: Add optional argument showfliers for boxenplot
2020-04-05 12:48:14,299 INFO #2000: Avoid floating point error with maximum husl sat/lum
2020-04-05 12:48:15,818 INFO #1999: Fix `add_legend` to always populate `_legend`
...
```

`gh-cli-pulls` creates a CSV file as [seaborn-pulls.csv](https://github.com/kazamori/github-api-tools/raw/main/example/pulls/csv-files/seaborn-pulls.csv) about Pull Requests created by a user.

[vviewer](https://github.com/t2y/vviewer) show values with columns every one line vertically. It's useful to check data for a quick look.

```bash
$ vviewer --quoting all example/pulls/csv-files/seaborn-pulls.csv

##### line no: 1
------------------------------------------------------------------------
001: additions                    : 44
002: changed_files                : 3
003: changes                      : -16
004: closed_at                    :
005: comments                     : 1
006: review_comments              : 0
007: reviews_length               : 0
008: created_at                   : 2020-06-25 20:58:04
009: deletions                    : 60
010: elapsed_days                 : -1.0
011: elapsed_days_of_first_comment: 0.00832175925925926
012: html_url                     : https://github.com/mwaskom/seaborn/pull/2148
013: labels_                      :
014: merged                       : False
015: number                       : 2148
016: reviewers                    :
017: title                        : Dont add null columns in plot_data for unassigned semantics
018: user.login                   : mwaskom
------------------------------------------------------------------------
Enter to next line, or q (quit):
```

#### Note

* `elapsed_days_of_first_comment`: first comment is any of issue comments, review comments and grouped review comments.

### Scatter plot

You can see a scatter plot created by [seaborn-pulls.csv](https://github.com/kazamori/github-api-tools/raw/main/example/pulls/csv-files/seaborn-pulls.csv) by default.

![](https://github.com/kazamori/github-api-tools/raw/main/example/pulls/figures/sample-seaborn-scatter-pr-stats1.png)

`scatter` is like a sub command and takes several options to customize the plot.

```bash
$ gh-cli-pulls scatter --help
usage: gh-cli-pulls scatter [-h] [--alpha ALPHA] [--col COL]
                                 [--col_wrap COL_WRAP] [--height HEIGHT]

optional arguments:
  -h, --help           show this help message and exit
  --alpha ALPHA        set alpha parameter for relplot
  --col COL            set col parameter for relplot
  --col_wrap COL_WRAP  set col_wrap parameter for relplot
  --height HEIGHT      set height parameter for seaborn plot
```

### Box plot

![](https://github.com/kazamori/github-api-tools/raw/main/example/pulls/figures/sample-box-pr-stats1.png)

`box` is like a sub command and takes several options to customize the plot.

```bash
$ gh-cli-pulls box --help
usage: gh-cli-pulls box [-h] [--height HEIGHT] [--width WIDTH]

optional arguments:
  -h, --help       show this help message and exit
  --height HEIGHT  set height parameter for subplots
  --width WIDTH    set width parameter for subplots
```

### Violin plot

![](https://github.com/kazamori/github-api-tools/raw/main/example/pulls/figures/sample-violin-pr-stats1.png)

`violin` is like a sub command and takes several options to customize the plot.

```bash
$ gh-cli-pulls violin --help
usage: gh-cli-pulls violin [-h] [--height HEIGHT] [--inner INNER]
                                [--loc LOC] [--width WIDTH]

optional arguments:
  -h, --help       show this help message and exit
  --height HEIGHT  set height parameter for subplots
  --inner INNER    set inner parameter for violinplot
  --loc LOC        set loc parameter for legend
  --width WIDTH    set width parameter for subplots
```

## Reference

* https://developer.github.com/v3/
* https://github.com/PyGithub/PyGithub
* https://seaborn.pydata.org/
