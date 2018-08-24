import filters
from skimage import color, io
from segmentation import generate_texture

def bitmap2material(img, expand_nmap=False, verbose=False):

    if verbose:
        print('Start processing...', flush=True)

    if verbose:
        print('Making seamless texture...', flush=True)
    img = filters.make_seamless(img)
    gray_img = color.rgb2gray(img)
    if verbose:
        print('...done', flush=True)
        io.imshow(img)
        io.show()

    if verbose:
        print('Computing normal map...', flush=True)
    n_map = filters.sobel_rgb_decoded(gray_img)
    if verbose:
        print('...done', flush=True)
        io.imshow(n_map)
        io.show()

    if expand_nmap:
        # works rather slowly, so just optional
        if verbose:
            print('Applying expansion filter to normal map...', flush=True)
        n_map = filters.norm_expansion(n_map, verbose=True)
        if verbose:
            print('...done', flush=True)
            io.imshow(n_map)
            io.show()

    if verbose:
        print('Computing bump map...', flush=True)
    bump_map = filters.bump_from_normal(n_map, initial_value=gray_img, verbose=False)[0]
    if verbose:
        print('...done', flush=True)
        io.imshow(bump_map)
        io.show()

    if verbose:
        print('Making Ambient Occlusion map...', flush=True)
    ao_map = filters.ambient_occlusion(bump_map, n_map, verbose=True)
    if verbose:
        print('...done', flush=True)
        io.imshow(ao_map, cmap='gray')
        io.show()

    if verbose:
        print('Making specular map...', flush=True)
    specular_map = filters.make_specular_map(gray_img)
    if verbose:
        print('...done', flush=True)
        io.imshow(specular_map, cmap='gray')
        io.show()

    if verbose:
        print('...ready!', flush=True)

    return (img, n_map, bump_map, ao_map, specular_map)


def process_image(img, verbose=False):
    if verbose:
        print('Step 1: texture creation.', flush=True)
    texture = generate_texture(img, verbose=verbose)

    if verbose:
        print('Step 2: texture to material.', flush=True)
    return bitmap2material(texture, verbose=verbose)


if __name__ == "__main__":

    path = input('Enter image name/path: ')
    #path = '../data/test_sobel.jpg'

    try:
        img = io.imread(path)
    except FileNotFoundError:
        print('File don\'t exist!')

    bitmap2material(img, verbose=True)
