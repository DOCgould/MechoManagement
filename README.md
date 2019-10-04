# Official Resource and Project Page for Mechatronics Software team

>In preparing for battle I have always found that plans are useless, but planning is indispensable.
-- Dwight D. Eisenhower

-- -
## Purpose
* Make Turning in Work Simple
* Make Turning in Work Automated
* Make Turnover Time Shorter

## Coding Style and Formatting Guide

#### For Python Code( same as last year )
* [PEP8](https://www.python.org/dev/peps/pep-0008/)

#### For C Code
* [Linux Kernel Coding Style( only look at relevant parts please )](https://www.kernel.org/doc/html/v4.10/process/coding-style.html#)
#### For GIT
* [Git Workflow](https://guides.github.com/introduction/flow/)
* [Git Ticketing](https://github.com/MichaelMure/git-bug)
* [Commit Messages](https://gist.github.com/robertpainsi/b632364184e70900af4ab688decf6f53)
* [Adding issuenumbers(refs)](https://guides.github.com/features/issues/) 
(This Will Be Continuously updated, but this should be a basis for now)
## completed deliverables
 - [x] inverted pendulum( pygame )

## upcoming deliverables
**Quadrotor LQR Controller ( pygame )**
```diff
- due: oct 12-24th
```
 - [ ] Python Based Controller ( pid or lqr )
    * Must be simulated with pygame ( experimental points for doing it with blender )
    * Must Indicate Equations of Motion( Latex is Optimal )

 - [ ] Can be in C++/C
    * Using C++11/C99
    * Must be Ported to Python
    * Must be Easy to use and Well Document( see above for details )

 - [ ] Python Optimization Libraries are allowed
    * scipy
    * numpy
    * control( fine, but see if it exists in the above first )
    * nobody wants to install yet *MORE* dependencies on my computer thanks ( management )

**GigE Vision Driver**
```diff
- due October 12th
```
**Linux Config(RTOS)**
```diff
- due: October 12th
```
**C/C++ Software Exam**
```diff
- due: October 19th
```
**Make the Pendulum or Quadrotor in Blender**
```diff
- due: October 12th
```
## Other Useful Resources
 * [Steve Brunton's Video Lecture Series](https://www.youtube.com/watch?v=1_UobILf3cc)
 * [Python version of Numerical Recipies in C](http://www-personal.umich.edu/~mejn/computational-physics/)
 * [ALL THE BOOKS](https://libgen.is/)
## Turning it All in
-- -
1. If you haven't already, download the git repo
    ```bash
    ~$ git clone https://github.com/DOCgould/MechoManagement.github.io
    ```
2. Navigate to the Folder Named: **preliminarySoftwareProjects/invertedPendulum/.**
3. Create a Directory with your name **firstnameLastname** *(camelcase)*
4. Upload your Files Before the Deadline

## How to Pull Changes from Master onto your Current Branch
1. Check and see what branch you are on
```bash
git status
```
2. If you are not on the branch you're trying to merge into, switch to that branch
```bash
git checkout dev/yournamehere
```
3. now that you are on the correct branch, Merge from Master
```
git merge origin/master
```

## Build Flow
#### From source to Module
1. Create CPython Source Files
    ```C
    '''
    This is the  spammodule, it does nothing but show an example
    '''
    #include <Python.h>
    
    static PyObject * spam_system(PyObject *self, PyObject *args){
        const char *command;
        int sts;
    
        if (!PyArg_ParseTuple(args, "s", &command))
            return NULL;
        sts = system(command);
        return PyLong_FromLong(sts);
    }
    
    static PyMethodDef SpamMethods[] = {
        {"system",  spam_system, METH_VARARGS,
         "Execute a shell command."},
        {NULL, NULL, 0, NULL}        /* Sentinel */
    };
    
    static struct PyModuleDef spammodule = { PyModuleDef_HEAD_INIT,
                                             "spam", /* name of module */
                                             NULL,   /* module documentation, may be NULL */
                                             -1,     /* size of per-interpreter state of the module,
                                                        or -1 if the module keeps state in global variables. */
                                             SpamMethods};
    
    PyMODINIT_FUNC PyInit_spam(void){
        PyObject *m;
        
        m = PyModule_Create(&spammodule);
        if (m == NULL)
            return NULL;
    
        return m;
    }
    
    ```
    (a) Using [setup.py](https://docs.python.org/3/extending/building.html#building) for buildinfo
    ```python
    from distutils.core import setup, Extension

    spam = Extension('spam', sources = ['spammodule.c'])

    setup (name = 'spammodule',
               version = '1.0',
                      description = 'This is a demo package',
                             ext_modules = [spam])
    ```
2. Create the build files from CPython Source
    ```bash
    python setup.py build
    ```
3. (Alternative) Create the Source Tarball
    ```bash
    python3 setup.py sdist
    ```
     Name of Build Tarball instead of 'PackageName'
     ```bash
    pip install spammodule-1.0
     ```
4. utilize [twine](https://pypi.org/project/twine/) for upload to pypi community

## How to Reference a Ticket in Your Commits
1. If you haven't already done so, please try out [git-bug](https://github.com/MichaelMure/git-bug)
2. When you want to reference a particular ticket, simply #(ticketnumber)
3. Example: I can Reference the Pendulum Deliverable #6 like so
