from email.message import Message
from typing import (
    TYPE_CHECKING,
    Text,
    List,
    Optional,
    Union,
    SupportsInt
)

from sifter.grammar.command import Command
from sifter.grammar.command_list import CommandList
import sifter.grammar
import sifter.handler
from sifter.validators.stringlist import StringList
from sifter.grammar.state import EvaluationState
from sifter.grammar.actions import Actions

if TYPE_CHECKING:
    from sifter.grammar.tag import Tag as TagGrammar
    from sifter.grammar.string import String
    from sifter.grammar.test import Test


# section 3.2
class CommandRequire(Command):

    RULE_IDENTIFIER: Text = 'REQUIRE'
    POSITIONAL_ARGS = [StringList()]

    def __init__(
        self,
        arguments: Optional[List[Union['TagGrammar', SupportsInt, List[Union[Text, 'String']]]]] = None,
        tests: Optional[List['Test']] = None,
        block: Optional[CommandList] = None
    ) -> None:
        super().__init__(arguments, tests, block)
        self.ext_names = self.positional_args[0]

    def evaluate(self, message: Message, state: EvaluationState) -> Optional[Actions]:
        for ext_name in self.ext_names:
            if not sifter.handler.get('extension', ext_name):
                raise RuntimeError(
                    "Required extension '%s' not supported"
                    % ext_name
                )
            state.require_extension(ext_name)
        return None


CommandRequire.register()
