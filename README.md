# cf_parallelizer

### The macro helps to deal with AWS API throttling during creating a lot of resources via cloudformation.

You can manually specify in how many threads your infrastructure will be deployed by setting "ParallelTaskQuantity" in the root of your template.
Also, it is possible to specify common dependencies which will be applied for all template resources by setting "CommonDependancies" array in the root of your template.
Do not forget to add the "Transform" statement in your processing template and point the macro "ParallelizerMacro".