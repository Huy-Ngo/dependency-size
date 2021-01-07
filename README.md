# Dependency resolver

This project is a study on how a package manager, such as pip or apt, resolve dependency and calculate the extra disk space required for installation of a new package. This is a part of a school project about graph theory.

### Problem

Calculate the total extra disk space needed to install a package.

Package managers such as pip or apt usually inform the user the total disk space that will be used for the package installation. This can be done by generating a tree from the dependency graph. In this project, we attempt to create a simulation of that feature.

### Specification

- Input: dependency graph, existing packages, package to be installed
- Output: the extra disk space needed 

### Assumptions

This project assumes the user is using a GNU/Linux distribution on a x86_64 machine, and have all Python version needed on their machine. This would specify which package release the user should install, that is, `manylinux1_x86_64` if it is released, else `sdist`.

### Dataset

We use data provided by PyPI API.

The information about a package will be find at `https://pypi.org/pypi/{package name}/{package version}/json`

### Example

Given the following dependency graph:

![eg-dependency](http://www.plantuml.com/plantuml/png/SoWkIImgAStDuIf8JCvEJ4zLK38qCF1rKb98B5PmH0YQm0MT48B6fZ11PuIW4Lob2pRjhjW4tRYu71LizFI0vZYXq2uG6gZ06KG3TRj0QOVKl1IWim40)

(Arrows denote dependency; for example: C --> A means C depends on A)

Let's say the user is going to install package E.

1. If the user has no packages

$$
Output = 400 (\text E) + 350(\text C) + 200 (\text D) + 100 (\text A) + 400 (\text B) \\
= 1450 (\text{MB})
$$

2. If the user has package C installled, which mean A and B are already installed as well:

$$ Output = 400 (\text E) + 200 (\text D) = 600 (\text{MB})$$

In reality, the situation is much more complicated: each package has many release; each release has different dependency; each dependency is not necessarily depends on one version of package, but maybe depend on any in a group of release, and it might not be latest.

![scipy-dep](https://www.planttext.com/api/plantuml/img/ZTBD2eCm303WUvuY-035gdK_E1sxxo6ATawcLRGUPEpTfsMmRa8sUYZjbnIQv3WOsPkngG5gTJ5eMkohycgmg7gLcwhL09tCRx9Kw0NYVF9G3ZZaLJTn9bW4i8H9NTOAzTXqqzs9vy4htWfdF62SqF27-l_cnaoiE2II8_VfxGevXG658OKVjVFiVNgm8cnaeJgyKm-8D-vM63l_zRzKV9HohMuReY-DoTmDgLkoXJjNionxCMCC7lDwpznobThox359vbtfOi1MezHJcW8Sv_CyqKy0)
