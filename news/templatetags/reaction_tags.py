from django import template

register = template.Library()

@register.filter(name='count_reactions')
def count_reactions(reactions, reaction_type):
    """
    Считает количество реакций типа reaction_type в списке/QuerySet reactions.
    """
    if reactions is None:
        return 0
    return sum(1 for reaction in reactions if reaction.reaction_type == reaction_type)

