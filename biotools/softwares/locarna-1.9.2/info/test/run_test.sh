

set -ex



mlocarna --version
locarna --version
locarna_p --version
sparse --version
exparna_p --version
echo -e ">D10744\nGGAAAAUUGAUCAUCGGCAAGAUAAGUUAUUUACUAAAUAAUAGGAUUUAAUAACCUGGUGAGUUCGAAUCUCACAUUUUCCG" | locarna_rnafold_pp --in-loop --stacking --noLP -p0.5 |head -n3
exit 0
