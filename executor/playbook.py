from ansible import context
from ansible.inventory.manager import InventoryManager
from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader
from ansible.plugins.strategy.control import StateQueueManager
from ansible.vars.manager import VariableManager
from ansible.executor.playbook_executor import PlaybookExecutor


def _set_default_ctx():
    context.CLIARGS = ImmutableDict(
        tags={}, listtags=False, listtasks=False, listhosts=False, syntax=False,
        connection='ssh',
        module_path=None, forks=100, remote_user='xxx', private_key_file=None,
        ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None,
        scp_extra_args=None,
        become=True,
        become_method='sudo', become_user='root', verbosity=True, check=False,
        start_at_task=None,
    )


class ExecuteController:
    def __init__(self, playbook, inventory, executor_id: str, passwords: dict = None):
        self._id = executor_id
        self._playbook = playbook
        self._inventory = inventory
        self._passwords = passwords
        self._state_queue_manager = StateQueueManager(executor_id=self._id)
        _set_default_ctx()

    def run_playbook(self):
        load_manager = DataLoader()
        inventory_manager = InventoryManager(loader=load_manager, sources=self._inventory)
        variable_manager = VariableManager(loader=load_manager, inventory=inventory_manager)
        variable_manager.extra_vars.update({"executor_id": self._id})

        executor = PlaybookExecutor(
            playbooks=self._playbook,
            inventory=inventory_manager,
            variable_manager=variable_manager,
            loader=load_manager,
            passwords=self._passwords,
        )

        return executor.run()

    def stop_playbook(self):
        self._state_queue_manager.update_state("stop")

    def pause_playbook(self):
        self._state_queue_manager.update_state("pause")

    def restart_playbook(self):
        self._state_queue_manager.update_state("restart")

    def get_state_playbook(self):
        pass