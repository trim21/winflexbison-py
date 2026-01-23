cmake_minimum_required(VERSION 3.25)

project(winflexbison_python VERSION 2.5.25 LANGUAGES C)

set(UPSTREAM_SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/upstream)

# Keep runtime outputs together so the copied bison data sits beside the executables.
set(WFB_RUNTIME_OUTPUT_DIR ${CMAKE_BINARY_DIR}/bin)

# Target install location for scripts/executables as provided by scikit-build-core.
set(SKBUILD_SCRIPTS_DIR $ENV{SKBUILD_SCRIPTS_DIR})
if(NOT SKBUILD_SCRIPTS_DIR)
  message(WARNING "SKBUILD_SCRIPTS_DIR not set; defaulting to CMAKE_INSTALL_BINDIR")
  set(SKBUILD_SCRIPTS_DIR ${CMAKE_INSTALL_BINDIR})
endif()

# Default to a Release build for single-config generators.
if(NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE "Release" CACHE STRING "Build type" FORCE)
endif()

# Build upstream as a subdirectory to reuse its targets without its install rules.
add_subdirectory(${UPSTREAM_SOURCE_DIR} upstream-build)

# Consolidate executable output locations for predictable packaging.
foreach(target win_flex win_bison)
  if(TARGET ${target})
    set_target_properties(${target} PROPERTIES
      RUNTIME_OUTPUT_DIRECTORY ${WFB_RUNTIME_OUTPUT_DIR}
      RUNTIME_OUTPUT_DIRECTORY_RELEASE ${WFB_RUNTIME_OUTPUT_DIR}
      RUNTIME_OUTPUT_DIRECTORY_DEBUG ${WFB_RUNTIME_OUTPUT_DIR}
    )
  endif()
endforeach()

# Install the executables into the interpreter's Scripts directory.
install(TARGETS win_flex win_bison RUNTIME DESTINATION ${SKBUILD_SCRIPTS_DIR})

# Install bison data directly into Scripts/data inside the wheel.
install(
  DIRECTORY ${UPSTREAM_SOURCE_DIR}/bison/data/
  DESTINATION ${SKBUILD_SCRIPTS_DIR}/data
  FILES_MATCHING
    PATTERN "*"
)

# Provide Flex headers for users who need them.
install(FILES ${UPSTREAM_SOURCE_DIR}/flex/src/FlexLexer.h DESTINATION winflexbison/include)

# Include Visual Studio custom build rules for users who rely on them.
install(DIRECTORY ${UPSTREAM_SOURCE_DIR}/custom_build_rules/ DESTINATION winflexbison/custom_build_rules)

# Bundle license information from upstream components.
install(FILES ${UPSTREAM_SOURCE_DIR}/COPYING DESTINATION winflexbison/licenses RENAME COPYING.winflexbison)
install(FILES ${UPSTREAM_SOURCE_DIR}/COPYING.DOC DESTINATION winflexbison/licenses)
install(FILES ${UPSTREAM_SOURCE_DIR}/bison/src/COPYING DESTINATION winflexbison/licenses RENAME COPYING.bison)
install(FILES ${UPSTREAM_SOURCE_DIR}/flex/src/COPYING DESTINATION winflexbison/licenses RENAME COPYING.flex)

# Include upstream documentation for reference.
install(FILES
  ${UPSTREAM_SOURCE_DIR}/README.md
  ${UPSTREAM_SOURCE_DIR}/changelog.md
  DESTINATION winflexbison/doc
)
