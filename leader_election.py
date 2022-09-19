import sys
import time
from kazoo.client import KazooClient, KazooState
from kazoo.protocol.states import EventType, WatchedEvent

ZNODE_PREFIX = '/a_'

class LeaderElection():
    def __init__(self, zooKeeperAddresses, nodeName, electionNamespace):
        self.zooKeeperAddresses = zooKeeperAddresses
        self.nodeName: str = nodeName
        self.electionNamespace = electionNamespace
        self.zk: KazooClient = None
        self._connect_zookeeper()
        self._leader = False


    @staticmethod
    def connection_status_listener(state):
        if state == KazooState.LOST:
            print('session to zookeeper was lost')  # Register somewhere that the session was lost
        elif state == KazooState.SUSPENDED:
            print('disconnected from zookeeper')  # Handle being disconnected from Zookeeper
        else:
            print('connected to zookeeper')  # Handle being connected/reconnected to Zookeeper

    def _connect_zookeeper(self):
        self.zk = KazooClient(hosts=self.zooKeeperAddresses)
        self.zk.start()
        self.zk.add_listener(self.connection_status_listener)  # notify about connection change


    def register(self):
        path = self.electionNamespace + ZNODE_PREFIX

        #create ephemeral Znode to represent the node (will create electionNamespace if not exists)
        new_node_path = self.zk.create(path=path, value=self.nodeName.encode(), ephemeral=True, sequence=True, makepath=True)
        self.znode_name = new_node_path.split('/')[-1]
        self.elect_leader()


    def elect_leader(self):
        print('leader_election: start')
        sorted_children = self.getchildrenlist()
        if sorted_children[0] == self.znode_name:
            self._leader = True
            while (1):
                update = input("Please insert 'Y' for get status of  flask Servers:\n")
                listchild=self.getchildrenlist()
                if update == "Y" or "y":
                    for child in listchild:
                        if sorted_children[0] == child:
                            print("This is the Leader: " + child + " Status: Online \n")
                        else:
                            print("The childern: " + child + " Status: Online \n")
        else:
            for child in sorted_children:
                if sorted_children[0] == child:
                    print("This is the Leader: " + child + " Status: Online \n")
                elif child == self.znode_name:
                    print("Im the childern: " + child + " Status: Online \n")
                else:
                    print("The childern: " + child + " Status: Online \n")
            predecessor_index = sorted_children.index(self.znode_name) -1
            print('Watching znode: ' + str(sorted_children[predecessor_index]))
            @self.zk.DataWatch(self.electionNamespace + '/' + sorted_children[predecessor_index])
            def register_next(data, stat, event):
                #race condition: it could be that the DataWatch failed as the predecessor node died during the time
                # between the get_children() and the DataWatch registration
                #to identify a failed watch registration: check that all the function params are None
                if data is None and stat is None:
                    #watch registration failed
                    self.elect_leader()
                    return
                if event is not None:
                    if event.type == EventType.DELETED:
                        print("Event is " + str(event))
                        self.elect_leader()


    def clean_zookeeper(self):
        self.zk.delete(self.electionNamespace, recursive=True)

    def is_leader(self) -> bool:
        return self._leader

    def getchildrenlist(self):
        children = self.zk.get_children(path=self.electionNamespace)
        sorted_children = sorted(children)
        return sorted_children

    def __repr__(self):
        return 'Leader ' if self._leader is True else '' + self.nodeName + '(' + self.znode_name + ')'


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('use leader_election.py <appName>')
        exit(-1)
    appName = sys.argv[1]
    leaderElection: LeaderElection = LeaderElection('localhost:2181', appName, '/election')
    #leaderElection.clean_zookeeper()

    leaderElection.register()

    try:
        time.sleep(300)
    finally:
        print('\n node interrupted')
        leaderElection.zk.stop()
        leaderElection.zk.close()
        print('\n node is dead')



