#include <stdio.h>
#include <stdlib.h>
#include <hdf5.h>
#include "common.h"
#include "hdf5io.h"

struct StructPointerTest
{  
    int x;  
    int y;  
};  

struct StructPointerTest *test(int a, int b)
{  
    struct StructPointerTest *p = (struct StructPointerTest *)malloc(sizeof(struct StructPointerTest));
    p->x = a;  
    p->y = b;  
    return p;
} 

/*
 * Function name: *HDF5IO(open_file)
 * @param[in] *fname
 * @Param[in] nWfmPerChunk
 * @Param[in] nCh
 * @return: a pointer of struct HDF5IO(waveform_file) data-type
 */
struct HDF5IO(waveform_file) *HDF5IO_open_file(const char *fname,
                                                size_t nWfmPerChunk,
                                                size_t nCh)
{
    hid_t rootGid, attrSid, attrAid;
    herr_t ret;

    struct HDF5IO(waveform_file) *wavFile;
    wavFile = (struct HDF5IO(waveform_file) *)
        malloc(sizeof(struct HDF5IO(waveform_file)));
    /* H5F_ACC_TRUNC: overwrite an existing file 
     * File Creation property list: H5P_DEFAULT
     * File access property list: H5P_DEFAULT
     */
    wavFile->waveFid = H5Fcreate(fname, H5F_ACC_TRUNC, H5P_DEFAULT, H5P_DEFAULT);
    wavFile->nWfmPerChunk = nWfmPerChunk;
    wavFile->nCh = nCh;
    /* H5Gopen: opens an existing group in a file
     * @param[in] loc_id: file or  group identifier specifying the location of the group to be opened
     * @param[in] name: name of the group to open
     * @param[in] gapl_id: Group access property list identifier
     */
    rootGid = H5Gopen(wavFile->waveFid, "/", H5P_DEFAULT);

    wavFile->nEvents = 0; /* an initial value */

    /* H5Screate: Creates a new dataspace of a specified type
     * H5S_SCALAR: has a single element, through that element may be of a complex datatype
     */
    attrSid = H5Screate(H5S_SCALAR);
    /* H5Acreate: Creates an attribute attached to a specified object
     * @param[in] loc_id: Location or object identifier
     * @param[in] attr_name: attribute name
     * @param[in] type_id: attribute datatype identifier
     * @param[in] space_id: attribute dataspace identifier, 
     * @param[in] acpl_id: attribute creation property list identifier
     * @param[in] aapl_id: attribute access property list identifier
     */
    attrAid = H5Acreate(rootGid, "nEvents", H5T_NATIVE_HSIZE, attrSid,
                        H5P_DEFAULT, H5P_DEFAULT);
    /* H5Awrite: writes data to an attribute
     * @param[in] attr_id: identifier of an attribute to write
     * @param[in] mem_type_id: identifier fo the attribute datatype (in memory)
     * @param[in] *buf: data to be write 
     */
    ret = H5Awrite(attrAid, H5T_NATIVE_HSIZE, &(wavFile->nEvents));
    H5Sclose(attrSid);          /* Releases and terminates access to a dataspace */
    H5Aclose(attrAid);          /* Closes the specified attribute */

    attrSid = H5Screate(H5S_SCALAR);
    attrAid = H5Acreate(rootGid, "nWfmPerChunk", H5T_NATIVE_HSIZE, attrSid,
                        H5P_DEFAULT, H5P_DEFAULT);
    ret = H5Awrite(attrAid, H5T_NATIVE_HSIZE, &nWfmPerChunk);
    H5Sclose(attrSid);
    H5Aclose(attrAid);

    attrSid = H5Screate(H5S_SCALAR);
    attrAid = H5Acreate(rootGid, "nCh", H5T_NATIVE_HSIZE, attrSid,
                        H5P_DEFAULT, H5P_DEFAULT);
    ret = H5Awrite(attrAid, H5T_NATIVE_HSIZE, &nCh);
    H5Sclose(attrSid);
    H5Aclose(attrAid);
    H5Gclose(rootGid);

    wavFile->nPt = SCOPE_MEM_LENGTH_MAX;
    return wavFile;
}
/* *HDF5IO(open_file_for_read)
 * @param[in] *fname : hdf5 file name
 * return: a pointer of struct HDF5IO(waveform_file)
 */
struct HDF5IO(waveform_file) *HDF5IO_open_file_for_read(const char *fname)
{
    hid_t attrAid;
    herr_t ret;

    struct HDF5IO(waveform_file) *wavFile;
    wavFile = (struct HDF5IO(waveform_file) *)
        malloc(sizeof(struct HDF5IO(waveform_file)));
    wavFile->waveFid = H5Fopen(fname, H5F_ACC_RDONLY, H5P_DEFAULT);

    /* H5Aopen_by_name: Opens an attribute for an object by object name and attribute name
     * @param[in] loc_id: Location from which to find object to which attribute is attached
     * @param[in] *obj_name: Name of object to which attribute is attached, relative to loc_id
     * @param[in] *attr_name: Name of attribute to open
     * @param[in] aapl_id: Attribute access property list
     * @param[in] lapl_id: Link access property list
     */
    attrAid = H5Aopen_by_name(wavFile->waveFid, "/", "nEvents",
                              H5P_DEFAULT, H5P_DEFAULT);
    /* H5Aread: Reads an attribute
     * @param[in] attr_id: Identifier of an attribute to read
     * @param[in] mem_type_id: Identifier of the attribute datatype (in memory) 
     * @param[in] *buf: Buffer for data to be read 
     */
    ret = H5Aread(attrAid, H5T_NATIVE_HSIZE, &(wavFile->nEvents));
    H5Aclose(attrAid);

    attrAid = H5Aopen_by_name(wavFile->waveFid, "/", "nWfmPerChunk",
                              H5P_DEFAULT, H5P_DEFAULT);
    ret = H5Aread(attrAid, H5T_NATIVE_HSIZE, &(wavFile->nWfmPerChunk));
    H5Aclose(attrAid);

    attrAid = H5Aopen_by_name(wavFile->waveFid, "/", "nCh",
                              H5P_DEFAULT, H5P_DEFAULT);
    ret = H5Aread(attrAid, H5T_NATIVE_HSIZE, &(wavFile->nCh));
    H5Aclose(attrAid);

    wavFile->nPt = SCOPE_MEM_LENGTH_MAX;
    return wavFile;
}

/* HDF5IO(close): close hdf5 file 
 * @param[in] HDF5IO(waveform_file) *waveFile
 */
int HDF5IO_close_file(struct HDF5IO(waveform_file) *wavFile)
{
    herr_t ret;
    ret = H5Fclose(wavFile->waveFid);       /* Terminates access to an HDF5 file */
    free(wavFile);                          /* release wavFile pointer */
    return (int)ret;
}
/* HDF5IO(flush_file): Flushes all buffers associated with a file to disk
 * @param[in] HDF5IO(waveform_file) *waveFile
 */
int HDF5IO_flush_file(struct HDF5IO(waveform_file) *wavFile)
{
    hid_t attrAid;
    herr_t ret;

    attrAid = H5Aopen_by_name(wavFile->waveFid, "/", "nEvents",
                              H5P_DEFAULT, H5P_DEFAULT);
    ret = H5Awrite(attrAid, H5T_NATIVE_HSIZE, &(wavFile->nEvents));
    H5Aclose(attrAid);
    /* H5Fflush: flushes all buffers associated with a file to disk
     * @param[in] object_id: Identifier of object used to identify the file
     * @param[in] scope: Specifies the scope of the flushing action, H5F_SCOPE_GLOBAL: flushes the entire virtual file, H5F_SCOPE_LOCAL: flushes only the specified file
     */
    ret = H5Fflush(wavFile->waveFid, H5F_SCOPE_GLOBAL);
    return (int)ret;
}
/* HDF5IO(write_waveform_attribute_in_file_header): 
 * @param[in] struct HDF5IO(waveform_file) *waveFile
 * @param[in] struct waveform_attribute *wavAttr
 */
int HDF5IO_write_waveform_attribute_in_file_header(
    struct HDF5IO(waveform_file) *wavFile,
    struct waveform_attribute *wavAttr)
{
    herr_t ret;
    
    hid_t wavAttrTid, wavAttrSid, wavAttrAid, doubleArrayTid, rootGid;
    const hsize_t doubleArrayDims[1]={SCOPE_NCH};   /* this variable comes from HDF5 and represents a native multiple-precision integer */
    const unsigned doubleArrayRank = 1;
    /* H5Tarray_create: Create an array datatype object
     * @param[in] base_type_id: Datatype identifier for the array base datatype
     * @param[in] rank: rank of the array
     * @param[in] dims[]: Size fo each array dimension
     */
    doubleArrayTid = H5Tarray_create(H5T_NATIVE_DOUBLE, doubleArrayRank, doubleArrayDims);
    /* H5Tcreate: creates a new datatype
     * @param[in] class: class of datatype to create
     * @param[in] size: the unmber of bytes in the datatype to create 
     */
    wavAttrTid = H5Tcreate(H5T_COMPOUND, sizeof(struct waveform_attribute));
    /* H5Tinsert: Adds a new member to a compound datatype
     * @param[in] dtype_id: identifier of compound datatype to modify
     * @param[in] *name: Name of the field to insert 
     * @param[in] offset: Offset in memory structure of the field to insert
     * @param[in] field_id: Datatype identifier of the field to insert
     */
    H5Tinsert(wavAttrTid, "wavAttr.chMask", HOFFSET(struct waveform_attribute, chMask), H5T_NATIVE_UINT);

    H5Tinsert(wavAttrTid, "wavAttr.nPt", HOFFSET(struct waveform_attribute, nPt), H5T_NATIVE_HSIZE);
    H5Tinsert(wavAttrTid, "wavAttr.nFrames", HOFFSET(struct waveform_attribute, nFrames), H5T_NATIVE_HSIZE);
    H5Tinsert(wavAttrTid, "wavAttr.dt", HOFFSET(struct waveform_attribute, dt), H5T_NATIVE_DOUBLE);
    H5Tinsert(wavAttrTid, "wavAttr.t0", HOFFSET(struct waveform_attribute, t0), H5T_NATIVE_DOUBLE);
    H5Tinsert(wavAttrTid, "wavAttr.ymult", HOFFSET(struct waveform_attribute, ymult), doubleArrayTid);
    H5Tinsert(wavAttrTid, "wavAttr.yoff", HOFFSET(struct waveform_attribute, yoff), doubleArrayTid);
    H5Tinsert(wavAttrTid, "wavAttr.yzero", HOFFSET(struct waveform_attribute, yzero), doubleArrayTid);
    /* Creates a new dataspace of a specified type
     * @param[in] H5S_SCALAR: a single element though that element may be of a complex datatype
     */
    wavAttrSid = H5Screate(H5S_SCALAR);
    
    rootGid = H5Gopen(wavFile->waveFid, "/", H5P_DEFAULT);
    wavAttrAid = H5Acreate(rootGid, "Waveform Attributes", wavAttrTid, wavAttrSid,H5P_DEFAULT, H5P_DEFAULT);

    ret = H5Awrite(wavAttrAid, wavAttrTid, wavAttr);

    H5Aclose(wavAttrAid);
    H5Sclose(wavAttrSid);
    H5Tclose(wavAttrTid);
    H5Tclose(doubleArrayTid);
    H5Gclose(rootGid);

    wavFile->nPt = wavAttr->nPt;
    return (int)ret;
}

int HDF5IO_read_waveform_attribute_in_file_header(
    struct HDF5IO(waveform_file) *wavFile,
    struct waveform_attribute *wavAttr)
{
    herr_t ret;
    hid_t rootGid;
    hid_t wavAttrTid, wavAttrAid, doubleArrayTid;
    const hsize_t doubleArrayDims[1]={SCOPE_NCH};
    const unsigned doubleArrayRank = 1;
    /* Creates an array datatype object
     * @param[in] base_type_id: Datatype identifier for the array base datatype
     * @param[in] rand: Rank of the array
     * @param[in] dims: Size of each array dimension 
     */
    doubleArrayTid = H5Tarray_create(H5T_NATIVE_DOUBLE, doubleArrayRank, doubleArrayDims);
    /* Creates a new datatype
     * @param[in] class: class of datatype to create [H5T_COMPOUND, H5T_OPAQUE, H5T_ENUM, H5T_STRING]
     * @param[in] size: the number of bytes in the datatype to create
     */
    wavAttrTid = H5Tcreate(H5T_COMPOUND, sizeof(struct waveform_attribute));

    H5Tinsert(wavAttrTid, "wavAttr.chMask", HOFFSET(struct waveform_attribute, chMask),
              H5T_NATIVE_UINT);
    H5Tinsert(wavAttrTid, "wavAttr.nPt", HOFFSET(struct waveform_attribute, nPt),
              H5T_NATIVE_HSIZE);
    H5Tinsert(wavAttrTid, "wavAttr.nFrames", HOFFSET(struct waveform_attribute, nFrames),
              H5T_NATIVE_HSIZE);
    H5Tinsert(wavAttrTid, "wavAttr.dt", HOFFSET(struct waveform_attribute, dt), H5T_NATIVE_DOUBLE);
    H5Tinsert(wavAttrTid, "wavAttr.t0", HOFFSET(struct waveform_attribute, t0), H5T_NATIVE_DOUBLE);
    H5Tinsert(wavAttrTid, "wavAttr.ymult",
              HOFFSET(struct waveform_attribute, ymult), doubleArrayTid);
    H5Tinsert(wavAttrTid, "wavAttr.yoff",
              HOFFSET(struct waveform_attribute, yoff), doubleArrayTid);
    H5Tinsert(wavAttrTid, "wavAttr.yzero",
              HOFFSET(struct waveform_attribute, yzero), doubleArrayTid);
    /* H5Aopen_by_name: opens an attribute for an object by object name and attribute name
     */
    wavAttrAid = H5Aopen_by_name(wavFile->waveFid, "/", "Waveform Attributes", H5P_DEFAULT, H5P_DEFAULT);
  
    /* H5Aread: Reads an attribute
     * @param[in] attr_id: identifier of an attribute to read
     * @param[in] mem_type_id: identifier of the attribute datatype (in memory)
     * @param[out] *buf: Buffer for data to be read
     */
    ret = H5Aread(wavAttrAid, wavAttrTid, wavAttr);

    H5Aclose(wavAttrAid);
    H5Tclose(wavAttrTid);
    H5Tclose(doubleArrayTid);

    wavFile->nPt = wavAttr->nPt;
    return (int)ret;
}

int HDF5IO_write_event(struct HDF5IO(waveform_file) *wavFile,
                        struct HDF5IO(waveform_event) *wavEvent)
{
    char buf[NAME_BUF_SIZE];
    herr_t ret;
    size_t chunkId, inChunkId;
    hid_t rootGid, chSid, chPid, chTid, chDid;
    hid_t mSid;
    hsize_t dims[2], h5chunkDims[2], slabOff[2], mOff[2], slabDims[2];
    
    chunkId = wavEvent->eventId / wavFile->nWfmPerChunk;
    inChunkId = wavEvent->eventId % wavFile->nWfmPerChunk;

    snprintf(buf, NAME_BUF_SIZE, "C%zd", chunkId);
    rootGid = H5Gopen(wavFile->waveFid, "/", H5P_DEFAULT);

#define write_event_create_dataset                   \
    do {                                                    \
        dims[0] = wavFile->nCh;                             \
        dims[1] = wavFile->nPt * wavFile->nWfmPerChunk;     \
        h5chunkDims[0] = 1;                                 \
        h5chunkDims[1] = wavFile->nPt;                      \
                                                            \
        chSid = H5Screate_simple(2, dims, NULL);            \
        chPid = H5Pcreate(H5P_DATASET_CREATE);              \
        H5Pset_chunk(chPid, 2, h5chunkDims);                \
        H5Pset_deflate(chPid, 6);                           \
                                                            \
        chTid = H5Tcopy(H5T_NATIVE_UCHAR);                   \
        chDid = H5Dcreate(rootGid, buf, chTid, chSid,       \
                          H5P_DEFAULT, chPid, H5P_DEFAULT); \
                                                            \
        H5Tclose(chTid);                                    \
        H5Pclose(chPid);                                    \
    } while(0)

    if(inChunkId == 0) { /* need to create a new chunk */
        write_event_create_dataset;
    } else {
        chDid = H5Dopen(rootGid, buf, H5P_DEFAULT);
        if(chDid < 0) { /* need to create a new chunk */
            /* This is not a neat way to do it.  One may check out
             * H5Lexists() and try to utilize that function.  Its
             * efficiency is not verified though. */
            write_event_create_dataset;
        } else {
            chSid = H5Dget_space(chDid);
        }
    }
#undef write_event_create_dataset

    slabOff[0] = 0;
    slabOff[1] = inChunkId * wavFile->nPt;
    slabDims[0] = wavFile->nCh;
    slabDims[1] = wavFile->nPt;
    H5Sselect_hyperslab(chSid, H5S_SELECT_SET, slabOff, NULL, slabDims, NULL);

    mSid = H5Screate_simple(2, slabDims, NULL);
    mOff[0] = 0;
    mOff[1] = 0;
    H5Sselect_hyperslab(mSid, H5S_SELECT_SET, mOff, NULL, slabDims, NULL);
    
    ret = H5Dwrite(chDid, H5T_NATIVE_UCHAR, mSid, chSid, H5P_DEFAULT,
                   wavEvent->wavBuf);
    //printf("%s\n", &wavEvent->wavBuf);
    wavFile->nEvents++;

    H5Sclose(mSid);
    H5Sclose(chSid);
    H5Dclose(chDid);
    H5Gclose(rootGid);
    return (int)ret;
}

/* HDF5IO_read_event
 * @param[in] wavFile: struct of HDF5IO_waveform_file
 * @param[in] waveEvent: struct of HDF5IO_waveform_event
 */
int HDF5IO_read_event(struct HDF5IO(waveform_file) *wavFile,
                       struct HDF5IO(waveform_event) *wavEvent)
{
    char buf[NAME_BUF_SIZE];
    herr_t ret;
    size_t chunkId, inChunkId;
    hid_t chSid, chDid;
    hid_t mSid;
    hsize_t slabOff[2], mOff[2], slabDims[2];
    chunkId = wavEvent->eventId / wavFile->nWfmPerChunk;
    inChunkId = wavEvent->eventId % wavFile->nWfmPerChunk;

    snprintf(buf, NAME_BUF_SIZE, "/C%zd", chunkId);
    /* H5Dopen: opens an existing dataset
     * @param[in] loc_id: identifier fo the file or group within the dataset to be accessed will be found
     * @param[in] name: Dataset name
     * @param[in] dapl_id: Dataset access property list
     */
    chDid = H5Dopen(wavFile->waveFid, buf, H5P_DEFAULT);
    /* H5Dget_space: Returns an identifier for a copy of the dataspace for a dataset
     * @param[in] dataset_id: identifier of the dataset to query
     * return a dataspace identifier if successful
     */
    chSid = H5Dget_space(chDid);

    slabOff[0] = 0;
    slabOff[1] = inChunkId * wavFile->nPt;
    slabDims[0] = wavFile->nCh;
    slabDims[1] = wavFile->nPt;
    /* H5Sselect_hyperslab: selects a hyperslab region to add to the current selected region
     * space_id: identifier of dataspace selection to modify
     * op: Operation to perform on current selection 
     * start: offset of start of hyperslab
     * count: number of blocks include in hyperslab
     * stride: hyperslab stride
     * block: size of block in hyperslab
     */
    H5Sselect_hyperslab(chSid, H5S_SELECT_SET, slabOff, NULL, slabDims, NULL);
    /* H5Screate_simple: Creates a new simple dataspace and opens it for access
     * @param[in] rank: number of dimensions of dataspace
     * @param[in] current_dims: array specifying the size of each dimension
     * @param[in] maximum_dims: array specifying the maximum size of each dimension
     */
    mSid = H5Screate_simple(2, slabDims, NULL);
    mOff[0] = 0;
    mOff[1] = 0;
    H5Sselect_hyperslab(mSid, H5S_SELECT_SET, mOff, NULL, slabDims, NULL);
    /* H5Dread: Reads raw data from a dataset into a buffer
     * @param[in] dataset_id: identifier of the dataset read from
     * @param[in] mem_type_id: identifier of the memory datatype
     * @param[in] mem_space_id: identifier of the memory dataspace
     * @param[in] file_space_id: identifier of the dataset's dataspace in the file
     * @param[in] xfer_plist_id: identifier of a transfer property list for this I/O operation
     * @param[out] buf: Buffer to receive data read from file
     */
    ret = H5Dread(chDid, H5T_NATIVE_UCHAR, mSid, chSid, H5P_DEFAULT, wavEvent->wavBuf);

    H5Sclose(mSid);
    H5Sclose(chSid);
    H5Dclose(chDid);
    return (int)ret;
}

size_t HDF5IO(get_number_of_events)(struct HDF5IO(waveform_file) *wavFile)
{
    /*
    herr_t ret;
    hid_t rootGid;
    H5G_info_t rootGinfo;
    size_t nEvents;
    
    rootGid = H5Gopen(wavFile->waveFid, "/", H5P_DEFAULT);
    ret = H5Gget_info(rootGid, &rootGinfo);
    nEvents = rootGinfo.nlinks;

    H5Gclose(rootGid);
    return nEvents;
    */
    return wavFile->nEvents;
}

#ifdef HDF5IO_DEBUG_ENABLEMAIN
int main(int argc, char **argv)
{
    int i;
    char array[20000]={1,2,3,4,5,
                       6,7,8,9,10,
                       11,12,13,14,15,
                       16,17,18,19,20};

    struct HDF5IO(waveform_file) *wavFile;
    struct waveform_attribute wavAttr = {
        .chMask = 0x0a,
        .nPt = 10000,
        .dt = 1e-6,
        .t0 = 0.0,
        .ymult = {1,1,1,1},
        .yoff = {0,0,0,0},
        .yzero = {0,0,0,0}
    };

    struct HDF5IO(waveform_event) evt = {
        .eventId = 0,
        .wavBuf = (char*)array
    };

    wavFile = HDF5IO(open_file)("test.h5", 4, 2);
    printf("wavFile->nWfmPerChunk = %zd\n", wavFile->nWfmPerChunk);
    printf("wavFile->nCh = %zd\n", wavFile->nCh);
    printf("wavFile->nPt = %zd\n", wavFile->nPt);
    HDF5IO(write_waveform_attribute_in_file_header)(wavFile, &wavAttr);
    printf("wavFile->nPt = %zd\n", wavFile->nPt);

    HDF5IO(write_event)(wavFile, &evt);
    evt.eventId = 1;
    HDF5IO(write_event)(wavFile, &evt);
    evt.eventId = 4;
    HDF5IO(write_event)(wavFile, &evt);
    evt.eventId = 8;
    HDF5IO(write_event)(wavFile, &evt);
    evt.eventId = 9;
    HDF5IO(write_event)(wavFile, &evt);

    HDF5IO(flush_file)(wavFile);
    HDF5IO(close_file)(wavFile);

    wavFile = HDF5IO(open_file_for_read)("test.h5");
    printf("number of events: %zd\n", HDF5IO(get_number_of_events)(wavFile));
    printf("wavFile->nWfmPerChunk = %zd\n", wavFile->nWfmPerChunk);
    printf("wavFile->nCh = %zd\n", wavFile->nCh);
    printf("wavFile->nPt = %zd\n", wavFile->nPt);
    HDF5IO(read_waveform_attribute_in_file_header)(wavFile, &wavAttr);
    printf("wavFile->nPt = %zd\n", wavFile->nPt);
    printf("number of events: %zd\n", HDF5IO(get_number_of_events)(wavFile));
    printf("%zd, %g, %g\n", wavAttr.nPt, wavAttr.dt, wavAttr.t0);

    for(i=0; i < wavFile->nCh * wavFile->nPt; i++) {
        evt.wavBuf[i] = 0;
    }
    evt.eventId = 1;
    HDF5IO(read_event)(wavFile, &evt);
    for(i=0; i < wavFile->nCh * wavFile->nPt; i++) {
        printf("%d ", evt.wavBuf[i]);
    }
    printf("\n");
    
    HDF5IO(close_file)(wavFile);
    
    return EXIT_SUCCESS;
}
#endif
