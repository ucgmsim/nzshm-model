import dataclasses
import hashlib
import json
import logging
import sys

import click

import nzshm_model
from nzshm_model import all_model_versions, get_model_version

log = logging.getLogger()
logging.basicConfig(level=logging.WARN)
logging.getLogger('nshm_toshi_client.toshi_client_base').setLevel(logging.INFO)
logging.getLogger('urllib3').setLevel(logging.INFO)
logging.getLogger('botocore').setLevel(logging.INFO)
logging.getLogger('gql.transport.requests').setLevel(logging.WARN)

formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
screen_handler = logging.StreamHandler(stream=sys.stdout)
screen_handler.setFormatter(formatter)
file_handler = logging.FileHandler('slt.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
log.addHandler(screen_handler)
log.addHandler(file_handler)


@click.group()
def slt():
    """Inspect and produce model source_logic_trees."""
    pass


@slt.command(name='ls')
@click.option('-l', '--long', is_flag=True, help="also print the model title.")
def cli_ls(long):
    """List the available model versions."""

    for version in all_model_versions():
        if not long:
            click.echo(version)
            continue
        model = nzshm_model.get_model_version(version)
        click.echo(f"{model.version} `{model.title}`")


@slt.command(name='to_json')
@click.argument('model_id')
def cli_model_as_json(model_id: str):
    """Get the model in json form."""
    model = get_model_version(model_id)
    j = json.dumps(dataclasses.asdict(model.source_logic_tree), indent=4)
    click.echo(j)


@slt.command(name='hash_sources')
@click.argument('model_id')
def cli_model_source_hashes(model_id: str):
    """Dump the sources with hashes."""
    model = get_model_version(model_id)
    for branch_set in model.source_logic_tree.branch_sets:
        for branch in branch_set.branches:
            nrmls = sorted([s.nrml_id for s in branch.sources])
            row = [ hashlib.shake_256(",".join(nrmls).encode()).hexdigest(6),
                    branch_set.short_name, branch.tag, nrmls, branch.weight ]
            click.echo(row)

@slt.command(name='hash_gmms')
@click.argument('model_id')
def cli_model_gmm_hashes(model_id: str):
    """Dump the gmm branches with hashes."""
    model = get_model_version(model_id)
    for branch_set in model.gmm_logic_tree.branch_sets:
        for branch in branch_set.branches:
            assert len(branch.uncertainty_models) == 1
            um_gmpe = branch.uncertainty_models[0].gmpe_name
            um_gmpe += ",".join(sorted(branch.uncertainty_models[0].arguments))

            row = [ hashlib.shake_256(um_gmpe.encode()).hexdigest(6),
                    branch_set.branchSetID, branch.branchID, um_gmpe, branch.uncertainty_weight, branch.uncertainty_models[0].arguments]
            click.echo(row)
            # nrmls = sorted([s.nrml_id for s in branch.sources])
            # row = [ hashlib.shake_256(",".join(nrmls).encode()).hexdigest(6),
            #         branch_set.short_name, branch.tag, nrmls, branch.weight ]
            # click.echo(row)

## gmlt.branch_sets[1].branches[-1].uncertainty_models[-1].text


# @slt.command(name='from_config')
# @click.argument('config_path')
# @click.argument('version')
# @click.argument('title')
# @click.option('-R', '--resolve_toshi_ids', is_flag=True)
# def cli_from_config(config_path, version, title, resolve_toshi_ids):
#     """Convert a python config file at CONFIG_PATH to an SLT model. Both VERSION and TITLE are required.

#     is this still required? Looks like it relates to old v1 SLTs
#     """

#     slt = from_config(config_path, version, title)

#     if resolve_toshi_ids:
#         slt = resolve_toshi_source_ids(slt)  # get new slt with toshi_ids
#     j = json.dumps(dataclasses.asdict(slt), indent=4)
#     click.echo(j)


# @slt.command(name='spec')
# @click.argument('model_id')
# @click.option('-B', '--build', is_flag=True)
# def cli_model_spec(model_id, build):
#     """Get a model specification by MODEL_ID."""
#     model = get_model_version(model_id)
#     if not model:
#         click.echo(f'Oops, the model "{model_id}" was not found', err=True)
#         return False
#     slt = model.source_logic_tree()
#     j = json.dumps(dataclasses.asdict(slt.derive_spec()), indent=4)
#     click.echo(j)


if __name__ == '__main__':
    slt()  # pragma: no cover
