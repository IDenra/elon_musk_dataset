import json
from typing import List

from pydantic import BaseModel


class Replica(BaseModel):
    author: str
    serial_number: int
    phrase: str


class Interview(BaseModel):
    title: str
    url: str
    replicas: List[Replica]

    @staticmethod
    def from_json(json_line: str) -> 'Interview':
        interview = json.loads(json_line)
        interview['replicas'] = [Replica(**replica) for replica in interview['replicas']]
        return Interview(**interview)

    def squash_subsequent_replicas(self, sep: str = ' ') -> 'Interview':
        new_interview = self.copy()
        if len(self.replicas) == 0:
            return new_interview

        joint_replicas = [self.replicas[0]]
        for replica in self.replicas[1:]:
            if joint_replicas[-1].author == replica.author:
                joint_replicas[-1].phrase += f'{sep}{replica.phrase}'
            else:
                joint_replicas.append(replica)

        new_interview.replicas = joint_replicas
        return new_interview
