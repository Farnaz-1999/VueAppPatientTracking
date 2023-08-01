import { SelectedMarker } from "../store/markers/markers.model";
import { ExtractPropTypes, PropType, Ref } from "vue";
export interface DetailsSectionMixin {
    props: Readonly<ExtractPropTypes<{
        item: PropType<SelectedMarker>;
    }>>;
    containerRef: Ref<HTMLElement | undefined>;
}
